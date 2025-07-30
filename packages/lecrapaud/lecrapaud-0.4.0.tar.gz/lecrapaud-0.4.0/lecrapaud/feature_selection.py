import pandas as pd
import numpy as np
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time
from typing import Optional
from tqdm import tqdm
import warnings
from concurrent.futures import ProcessPoolExecutor, as_completed
import joblib
import re
from pathlib import Path

os.environ["COVERAGE_FILE"] = str(Path(".coverage").resolve())

# feature selection
from sklearn.feature_selection import (
    f_classif,
    f_regression,
    mutual_info_classif,
    mutual_info_regression,
    chi2,
    SelectPercentile,
    SelectFpr,
    RFE,
    SelectFromModel,
)
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import root_mean_squared_error, log_loss, make_scorer
from mlxtend.feature_selection import SequentialFeatureSelector
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
import category_encoders as ce
from scipy.stats import spearmanr, kendalltau

# Scaling
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Internal
from src.directory_management import tmp_dir, clean_directory
from src.utils import logger
from src.config import PYTHON_ENV
from src.db.models import (
    Dataset,
    Target,
    Feature,
    FeatureSelection,
    FeatureSelectionRank,
)
from src.db.setup import get_db

# Variables for targets handling
TARGETS_NUMBER = range(1, 15)
TARGETS_CLF = [2, 4, 6, 8, 9, 10, 11]
TARGETS_MCLF = [11]
GROUPING_COLUMN = "STOCK"
DATE_COLUMN = "DATE"

# Annoying Warnings
warnings.filterwarnings("ignore", category=FutureWarning)


def get_dataset_name(
    df, corr_threshold: int = 80, percentile: int = 20, max_features: int = 20
):
    number_of_groups = df[GROUPING_COLUMN].nunique()

    # Try to convert DATE column to datetime safely
    if pd.api.types.is_integer_dtype(df[DATE_COLUMN]):
        df_date = df[DATE_COLUMN].map(pd.Timestamp.fromordinal)
    else:
        df_date = pd.to_datetime(
            df[DATE_COLUMN], errors="coerce"
        )  # convert strings, datetime, etc.

    name = f"data_{number_of_groups}_{corr_threshold}_{percentile}_{max_features}_{df_date.min().date()}_{df_date.max().date()}"
    if PYTHON_ENV == "Test":
        name = f"test_{name}"
    return name


def create_sets_from_data(
    df: pd.DataFrame,
    corr_threshold: int = 80,
    percentile: int = 20,
    max_features: int = 20,
):

    df.sort_values([DATE_COLUMN, GROUPING_COLUMN], inplace=True)

    # Drop non-useful column for training
    if "ISIN" in df.columns:
        df.drop(labels=["ISIN"], axis=1, inplace=True)
    if "SECURITY" in df.columns:
        df.drop(labels=["SECURITY"], axis=1, inplace=True)

    dates = df[DATE_COLUMN].unique()

    val_first_id = int(len(dates) * 0.6) + 1
    test_first_id = int(len(dates) * 0.8) + 1

    train = df[df[DATE_COLUMN].isin(dates[:val_first_id])]
    val = df[df[DATE_COLUMN].isin(dates[val_first_id:test_first_id])]
    test = df[df[DATE_COLUMN].isin(dates[test_first_id:])]

    dates = {}
    dates["start_date"] = pd.to_datetime(df[DATE_COLUMN].iat[0])
    dates["end_date"] = pd.to_datetime(df[DATE_COLUMN].iat[-1])
    for name, data in zip(["train", "val", "test"], [train, val, test]):
        dates[f"{name}_start_date"] = pd.to_datetime(data[DATE_COLUMN].iat[0])
        dates[f"{name}_end_date"] = pd.to_datetime(data[DATE_COLUMN].iat[-1])

        logger.info(
            f"{len(data['DATE'])} {name} data from {dates[f"{name}_start_date"].strftime('%d/%m/%Y')} to {dates[f"{name}_end_date"].strftime('%d/%m/%Y')}"
        )

    datasets = {}

    with get_db() as db:
        all_targets = Target.get_all(db=db)
        matched_targets = [
            target for target in all_targets if target.name in train.columns
        ]
        dataset_name = get_dataset_name(train, corr_threshold, percentile, max_features)
        dataset_dir = f"{tmp_dir}/{dataset_name}"
        preprocessing_dir = f"{dataset_dir}/preprocessing"
        train_data_dir = f"{dataset_dir}/data"
        os.makedirs(dataset_dir, exist_ok=True)
        os.makedirs(preprocessing_dir, exist_ok=True)
        os.makedirs(train_data_dir, exist_ok=True)

        dataset = datasets[name] = Dataset.upsert(
            match_fields=["name"],
            db=db,
            name=dataset_name,
            path=Path(dataset_dir).resolve(),
            type="training",
            size=df.shape[0],
            train_size=train.shape[0],
            val_size=val.shape[0],
            test_size=test.shape[0],
            number_of_groups=data[GROUPING_COLUMN].nunique(),
            list_of_groups=data[GROUPING_COLUMN].unique().tolist(),
            corr_threshold=corr_threshold,
            percentile=percentile,
            max_features=max_features,
            **dates,
            targets=matched_targets,
        )

        # encode categoricals
        train = encode_categorical_features(train, fit=True, save_dir=preprocessing_dir)
        val = encode_categorical_features(val, save_dir=preprocessing_dir)
        test = encode_categorical_features(test, save_dir=preprocessing_dir)

        # save the full data
        if PYTHON_ENV != "Test":
            joblib.dump(df, f"{train_data_dir}/full.pkl")

        return train, val, test, dataset


def encode_categorical_features(df: pd.DataFrame, save_dir: str, fit: bool = False):

    X = df.loc[:, ~df.columns.str.contains("^TARGET_")]
    y = df.loc[:, df.columns.str.contains("^TARGET_")]

    # 1. Timestamps for 'DATE'
    X.loc[:, DATE_COLUMN] = pd.to_datetime(X[DATE_COLUMN]).map(pd.Timestamp.toordinal)

    if fit:
        # Define columns for ordinal and binary encoding (we should have all possible values in training set, unless we accept unknown values processing)
        ordinal_encoding_features = ["STOCK"]

        binary_encoding_features = ["SECTOR", "SUBINDUSTRY", "LOCATION"]

        # Fit and save the ColumnTransformer with OrdinalEncoder and OneHotEncoder
        column_transformer = ColumnTransformer(
            transformers=[
                (
                    "ordinal",
                    OrdinalEncoder(
                        handle_unknown="use_encoded_value",
                        unknown_value=-1,  # rows with unseen STOCK values will be encoded as -1
                    ),
                    ordinal_encoding_features,
                ),
                (
                    "binary_encoder",
                    ce.BinaryEncoder(
                        handle_unknown="value",
                    ),  # rows with unseen values will be encoded as all-zeros in the binary columns
                    binary_encoding_features,
                ),
            ],
            remainder="passthrough",  # Keep the non-encoded columns like 'DATE'
        )
        transformed_data = column_transformer.fit_transform(X)
        if PYTHON_ENV != "Test":
            joblib.dump(column_transformer, f"{save_dir}/column_transformer.pkl")
    else:
        # Load the ColumnTransformer and apply it
        column_transformer = joblib.load(f"{save_dir}/column_transformer.pkl")

        transformed_data = column_transformer.transform(X)

    # Convert to DataFrame for readability and return
    transformed_X = pd.DataFrame(
        transformed_data,
        columns=[
            feature.split("__")[1]
            for feature in column_transformer.get_feature_names_out()
        ],
        index=X.index,
    )
    transformed_X = transformed_X.apply(pd.to_numeric)
    for col in [
        feature.split("__")[1]
        for feature in column_transformer.get_feature_names_out()
        if "remainder" not in feature
    ] + [DATE_COLUMN]:
        transformed_X[col] = transformed_X[col].astype(int)

    # Insert features in db
    if fit:
        # TODO: in bulk
        for feature in transformed_X.columns:
            dtype = transformed_X[feature].dtype
            if pd.api.types.is_integer_dtype(dtype):
                feature_type = "categorical"
            elif pd.api.types.is_float_dtype(dtype):
                feature_type = "numerical"
            else:
                feature_type = "other"
            Feature.upsert(match_fields=["name"], name=feature, type=feature_type)
        for target in y.columns:
            type = (
                "classification"
                if int(target.split("_")[1]) in TARGETS_CLF
                else "regression"
            )
            # TODO: what about description here ?
            Target.upsert(match_fields=["name", "type"], name=target, type=type)

    return pd.concat([transformed_X, y], axis=1)


# only work with all features from feat eng in the right order (unused for now)
def decode_categorical_features(df: pd.DataFrame, save_dir: str):
    X = df.loc[:, ~df.columns.str.contains("^TARGET_")]
    y = df.loc[:, df.columns.str.contains("^TARGET_")]
    index = X.index
    original_dtypes = X.dtypes.to_dict()

    column_transformer = joblib.load(f"{save_dir}/column_transformer.pkl")

    X = X.to_numpy()
    arrays = []
    for name, indices in column_transformer.output_indices_.items():
        transformer = column_transformer.named_transformers_.get(name, None)
        arr = X[:, indices.start : indices.stop]

        if transformer in (None, "passthrough", "drop"):
            pass

        else:
            arr = transformer.inverse_transform(arr)

        arrays.append(arr)

    retarr = np.concatenate(arrays, axis=1)

    columns_ordinal = [
        feature.split("__")[1]
        for feature in column_transformer.get_feature_names_out()
        if feature.split("__")[0] == "ordinal"
    ]
    columns_binary_encoder = [
        feature.split("__")[1]
        for feature in column_transformer.get_feature_names_out()
        if feature.split("__")[0] == "binary_encoder"
    ]
    # Remove trailing "_number" using regex
    columns_binary_encoder = {
        re.sub(r"_\d+$", "", col) for col in columns_binary_encoder
    }
    columns_binary_encoder = list(columns_binary_encoder)

    columns_remainder = [
        feature.split("__")[1]
        for feature in column_transformer.get_feature_names_out()
        if feature.split("__")[0] == "remainder"
    ]
    columns = columns_ordinal + columns_binary_encoder + columns_remainder
    decoded_X = pd.DataFrame(
        retarr,
        columns=columns,
        index=index,
    )

    for col in decoded_X.columns:
        if col in columns_ordinal or col in columns_binary_encoder:
            decoded_X[col] = decoded_X[col].astype(str)
        elif col in original_dtypes:
            decoded_X[col] = decoded_X[col].astype(original_dtypes[col])

    # revert timestamps to dates
    decoded_X.loc[:, DATE_COLUMN] = decoded_X[DATE_COLUMN].map(pd.Timestamp.fromordinal)

    return pd.concat([decoded_X, y], axis=1)


# Filter methods
# ----------------


# Linear correlation (Person's R for regression and ANOVA for classification)
def select_feature_by_linear_correlation(
    X, y, target_type, percentile: int = 20, save_dir: Optional[str] = None
):
    start = time.time()
    test_type = "Person’s R" if target_type == "regression" else "ANOVA"
    logger.debug(f"Running {test_type}...")

    model = f_regression if target_type == "regression" else f_classif
    feat_selector = SelectPercentile(model, percentile=percentile).fit(X, y)
    feat_scores = pd.DataFrame()
    feat_scores["score"] = feat_selector.scores_
    feat_scores["pvalue"] = feat_selector.pvalues_
    feat_scores["support"] = feat_selector.get_support()
    feat_scores["features"] = X.columns
    feat_scores["rank"] = feat_scores["score"].rank(method="first", ascending=False)
    feat_scores["method"] = test_type
    feat_scores.sort_values("rank", ascending=True, inplace=True)
    stop = time.time()
    training_time = timedelta(seconds=(stop - start)).total_seconds()
    feat_scores["training_time"] = training_time

    logger.debug(
        f"{test_type} evaluation selected {feat_scores['support'].sum()} features in {training_time:.2f} seconds"
    )

    feat_scores.to_csv(
        f"{save_dir}/{test_type}.csv",
        index=True,
        header=True,
        index_label="ID",
    )

    return feat_scores


# Non-Linear correlation (Spearsman's R for regression and Kendall’s Tau for classification)
def select_feature_by_nonlinear_correlation(
    X, y, target_type, percentile: int = 20, save_dir: Optional[str] = None
):
    start = time.time()

    def model(X_model, y_model):
        X_model = pd.DataFrame(X_model)
        y_model = pd.Series(y_model)

        method = "spearman" if target_type == "regression" else "kendall"

        corr_scores = []
        p_values = []

        for col in X_model.columns:
            if method == "spearman":
                corr, pval = spearmanr(X_model[col], y_model)
            else:  # Kendall's Tau for classification
                corr, pval = kendalltau(X_model[col], y_model)

            corr_scores.append(abs(corr))  # Keeping absolute correlation
            p_values.append(pval)

        return np.array(corr_scores), np.array(p_values)

    test_type = "Spearman’s R" if target_type == "regression" else "Kendall’s Tau"
    logger.debug(f"Running {test_type}...")

    feat_selector = SelectPercentile(model, percentile=percentile).fit(X, y)
    feat_scores = pd.DataFrame()
    feat_scores["score"] = feat_selector.scores_
    feat_scores["pvalue"] = feat_selector.pvalues_
    feat_scores["support"] = feat_selector.get_support()
    feat_scores["features"] = X.columns
    feat_scores["rank"] = feat_scores["score"].rank(method="first", ascending=False)
    feat_scores["method"] = test_type
    feat_scores.sort_values("rank", ascending=True, inplace=True)
    stop = time.time()
    training_time = timedelta(seconds=(stop - start)).total_seconds()
    feat_scores["training_time"] = training_time

    logger.debug(
        f"{test_type} evaluation selected {feat_scores['support'].sum()} features in {training_time:.2f} seconds"
    )

    feat_scores.to_csv(
        f"{save_dir}/{test_type}.csv",
        index=True,
        header=True,
        index_label="ID",
    )

    return feat_scores


# Mutual Information
def select_feature_by_mi(
    X, y, target_type, percentile: int = 20, save_dir: Optional[str] = None
):
    start = time.time()
    logger.debug("Running Mutual Information...")
    model = (
        mutual_info_regression if target_type == "regression" else mutual_info_classif
    )
    feat_selector = SelectPercentile(model, percentile=percentile).fit(X, y)
    feat_scores = pd.DataFrame()
    feat_scores["score"] = feat_selector.scores_
    feat_scores["support"] = feat_selector.get_support()
    feat_scores["features"] = X.columns
    feat_scores["rank"] = feat_scores["score"].rank(method="first", ascending=False)
    feat_scores["method"] = "Mutual Information"
    feat_scores.sort_values("rank", ascending=True, inplace=True)
    stop = time.time()
    training_time = timedelta(seconds=(stop - start)).total_seconds()
    feat_scores["training_time"] = training_time

    logger.debug(
        f"MI evaluation selected {feat_scores['support'].sum()} features in {training_time:.2f} seconds"
    )

    feat_scores.to_csv(f"{save_dir}/MI.csv", index=True, header=True, index_label="ID")

    return feat_scores


def select_categorical_features(X, y, percentile, save_dir: Optional[str] = None):
    start = time.time()
    logger.debug("Running Chi2 for categorical features...")
    feat_selector = SelectPercentile(chi2, percentile=percentile).fit(X, y)
    feat_scores = pd.DataFrame()
    feat_scores["score"] = feat_selector.scores_
    feat_scores["pvalue"] = feat_selector.pvalues_
    feat_scores["support"] = feat_selector.get_support()
    feat_scores["features"] = X.columns
    feat_scores["rank"] = feat_scores["score"].rank(method="first", ascending=False)
    feat_scores["method"] = "Chi2"
    feat_scores.sort_values("rank", ascending=True, inplace=True)
    stop = time.time()
    training_time = timedelta(seconds=(stop - start)).total_seconds()
    feat_scores["training_time"] = training_time

    logger.debug(
        f"Chi2 evaluation selected {feat_scores['support'].sum()} features in {training_time:.2f} seconds"
    )

    feat_scores.to_csv(
        f"{save_dir}/Chi2.csv", index=True, header=True, index_label="ID"
    )

    return feat_scores


# Intrisic/embeedded method
# ----------------


# feature importance
def select_feature_by_feat_imp(
    X, y, target_type, percentile: int = 20, save_dir: Optional[str] = None
):
    start = time.time()
    logger.debug("Running Feature importance...")

    params = {"n_estimators": 500, "max_depth": 2**3, "random_state": 42, "n_jobs": -1}

    estimator = (
        RandomForestClassifier(**params)
        if target_type == "classification"
        else RandomForestRegressor(**params)
    )

    feat_selector = SelectFromModel(
        estimator=estimator,
        threshold=-np.inf,
        max_features=int(percentile * X.shape[1] / 100),
    ).fit(X, y)

    feat_scores = pd.DataFrame()
    feat_scores["score"] = feat_selector.estimator_.feature_importances_
    feat_scores["support"] = feat_selector.get_support()
    feat_scores["features"] = X.columns
    feat_scores["rank"] = feat_scores["score"].rank(method="first", ascending=False)
    feat_scores["method"] = "FI"
    feat_scores.sort_values("rank", ascending=True, inplace=True)

    stop = time.time()
    training_time = timedelta(seconds=(stop - start)).total_seconds()
    feat_scores["training_time"] = training_time

    logger.debug(
        f"Feat importance evaluation selected {feat_scores['support'].sum()} features in {training_time:.2f} seconds"
    )

    feat_scores.to_csv(f"{save_dir}/FI.csv", index=True, header=True, index_label="ID")

    return feat_scores


# Wrapper method
# ----------------


# recursive feature elimination
def select_feature_by_rfe(
    X, y, target_type, percentile: int = 20, save_dir: Optional[str] = None
):
    start = time.time()
    logger.debug("Running Recursive Feature Elimination...")

    params = {
        "max_depth": 2**3,
        "random_state": 42,
    }
    estimator = (
        DecisionTreeClassifier(**params)
        if target_type == "classification"
        else DecisionTreeRegressor(**params)
    )
    rfe = RFE(estimator, n_features_to_select=percentile / 100, step=4, verbose=0)
    feat_selector = rfe.fit(X, y)

    feat_scores = pd.DataFrame(
        {
            "score": 0.0,  # Default feature importance
            "support": feat_selector.get_support(),
            "features": X.columns,
            "rank": 0,
            "method": "RFE",
        }
    )
    feat_scores.loc[
        feat_scores["features"].isin(feat_selector.get_feature_names_out()), "score"
    ] = list(feat_selector.estimator_.feature_importances_)
    feat_scores["rank"] = feat_scores["score"].rank(method="first", ascending=False)
    feat_scores.sort_values("rank", ascending=True, inplace=True)

    stop = time.time()
    training_time = timedelta(seconds=(stop - start)).total_seconds()
    feat_scores["training_time"] = training_time

    logger.debug(
        f"RFE evaluation selected {feat_scores['support'].sum()} features in {training_time:.2f} seconds"
    )

    feat_scores.to_csv(f"{save_dir}/RFE.csv", index=True, header=True, index_label="ID")

    return feat_scores


# SequentialFeatureSelector (loss based, possibility to do forwards or backwards selection or removal)
def select_feature_by_sfs(
    X, y, target_type, percentile: int = 20, save_dir: Optional[str] = None
):
    start = time.time()
    logger.debug("Running Sequential Feature Selection...")
    warnings.filterwarnings("ignore", category=FutureWarning)

    params = {
        "max_depth": 2**3,
        "random_state": 42,
    }
    estimator = (
        DecisionTreeClassifier(**params)
        if target_type == "classification"
        else DecisionTreeRegressor(**params)
    )

    n_splits = 3
    n_samples = len(X)
    test_size = int(n_samples / (n_splits + 4))
    tscv = TimeSeriesSplit(n_splits=n_splits, test_size=test_size)

    score_function = (
        make_scorer(
            log_loss, response_method="predict_proba"
        )  # logloss needs probabilities
        if target_type == "classification"
        else make_scorer(root_mean_squared_error)
    )  # we avoid greater_is_better = False because it make the score negative and mess up ranking

    sfs = SequentialFeatureSelector(
        estimator,
        k_features=int(percentile * X.shape[1] / 100),
        forward=True,
        floating=True,  # Enables dynamic feature elimination
        scoring=score_function,
        cv=tscv,
        n_jobs=-1,
        verbose=0,
    )

    feat_selector = sfs.fit(X, y)

    # Extract selected features and their scores
    selected_features = set(feat_selector.k_feature_names_)
    feat_subsets = feat_selector.subsets_

    # Create DataFrame for feature scores
    feat_scores = pd.DataFrame(
        {
            "features": X.columns,
            "support": X.columns.isin(
                selected_features
            ),  # TODO: comprendre pourquoi le support n'est pas correct (les bons scores ne sont pas toujours choisis)
            "score": 1000,
            "rank": None,
            "method": "SFS",
        }
    )

    # Sort subsets by score (lower is better)
    sorted_subsets = sorted(feat_subsets.items(), key=lambda item: item[1]["avg_score"])

    # Record score per feature (first appearance)
    feature_score_map = {}
    for step in sorted_subsets:
        step = step[1]
        for feature in step["feature_names"]:
            if feature not in feature_score_map:
                feature_score_map[feature] = step["avg_score"]

    # Assign scores
    for feature, score in feature_score_map.items():
        feat_scores.loc[feat_scores["features"] == feature, "score"] = score

    # rank by score (lower = better)
    feat_scores["rank"] = (
        feat_scores["score"].rank(method="first", ascending=True).astype(int)
    )

    feat_scores.sort_values("rank", ascending=True, inplace=True)

    stop = time.time()
    training_time = timedelta(seconds=(stop - start)).total_seconds()
    feat_scores["training_time"] = training_time

    logger.debug(
        f"SFS evaluation selected {feat_scores['support'].sum()} features in {training_time:.2f} seconds"
    )

    feat_scores.to_csv(f"{save_dir}/SFS.csv", index=True, header=True, index_label="ID")

    return feat_scores


# Remove correlation
# ------------------


def remove_correlated_features(
    X: pd.DataFrame, features: list, corr_threshold: int, vizualize: bool = False
):
    # Create correlation matrix, select upper triangle & remove features with correlation greater than threshold
    corr_matrix = X[features].corr().abs()

    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
    features_uncorrelated = [
        column
        for column in upper.columns
        if all(upper[column].dropna() <= corr_threshold / 100)
    ]
    features_correlated = [
        column for column in upper.columns if any(upper[column] > corr_threshold / 100)
    ]

    if vizualize:
        features_selected_visualization = (
            X[features]
            .corr()
            .where(np.triu(np.ones(len(features)), k=1).astype(bool))
            .fillna(0)
        )
        # Plot the heatmap
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap="coolwarm",
            center=0,
            linewidths=1,
            linecolor="black",
        )
        plt.title(f"Correlation Matrix")
        plt.show()

        logger.info(f"\n{features_selected_visualization.describe().to_string()}")
        logger.info(f"\n{features_selected_visualization.to_string()}")
    return features_uncorrelated, features_correlated


# Main feature selection function
def feature_selection(
    dataset_id: int,
    train: pd.DataFrame,
    target_number: int,
    single_process: bool = False,
):
    """Function to do feature selection with a range of different feature selection technics

    Args:
        - train (pd.DataFrame): a pandas train set
        - target_number (in): a target, targets need to be name ``TARGET_{n}```
        - single_process (bool): if True, run all feature selection methods in a single process. If False, run them in parallel.
    """

    # Create the feature selection in db
    target = Target.find_by(name=f"TARGET_{target_number}")
    dataset = Dataset.get(dataset_id)
    percentile = dataset.percentile
    corr_threshold = dataset.corr_threshold
    max_features = dataset.max_features

    feature_selection = FeatureSelection.upsert(
        match_fields=["target_id", "dataset_id"],
        target_id=target.id,
        dataset_id=dataset.id,
    )

    X = train.loc[:, ~train.columns.str.contains("^TARGET_")]
    y = train[f"TARGET_{target_number}"]

    logger.info(f"Starting feature selection for TARGET_{target_number}...")

    target_type = "classification" if target_number in TARGETS_CLF else "regression"

    fs_dir_target = f"{dataset.path}/{y.name}/feature_selection"
    preprocessing_dir = f"{dataset.path}/preprocessing"
    os.makedirs(fs_dir_target, exist_ok=True)
    clean_directory(fs_dir_target)

    # Let's start by removing extremly correlated features
    # This is needed to reduce nb of feature but also for methods such as anova or chi2 that requires independent features
    # TODO: we could also remove low variance features
    features_uncorrelated, features_correlated = remove_correlated_features(
        X, X.columns, 90, vizualize=False
    )
    X = X[features_uncorrelated]

    logger.debug(
        f"""
        \nWe first have removed {len(features_correlated)} features with correlation greater than 90%
        \nWe are looking to capture {percentile}% of {len(X.columns)} features, i.e. {int(len(X.columns)*percentile/100)} features, with different feature selection methods
        \nWe will then remove above {corr_threshold}% correlated features, keeping the one with the best ranks
        \nFinally, we will keep only the {max_features} best ranked features
        """
    )

    start = time.time()

    # handling categorical features (only if classification)
    categorical_features = X.select_dtypes(include=["int64", "Int64"]).columns.tolist()
    X_categorical = X[categorical_features]

    if target_type == "classification":
        feat_scores = select_categorical_features(
            X_categorical, y, percentile, save_dir=fs_dir_target
        )
        with get_db() as db:
            for row in feat_scores.itertuples(index=False):
                feature = Feature.find_by(name=row.features, db=db)
                FeatureSelectionRank.upsert(
                    ["feature_selection_id", "feature_id", "method"],
                    db=db,
                    score=row.score,
                    pvalue=row.pvalue,
                    support=row.support,
                    rank=row.rank,
                    method=row.method,
                    training_time=row.training_time,
                    feature_selection_id=feature_selection.id,
                    feature_id=feature.id,
                )
        categorical_features_selected = feat_scores[feat_scores["support"] == True][
            "features"
        ].values.tolist()

    # removing categorical features from X
    numerical_features = list(set(X.columns).difference(set(categorical_features)))
    X_numerical = X[numerical_features]

    results = []
    if single_process:
        results = [
            select_feature_by_linear_correlation(
                X_numerical, y, target_type, percentile, save_dir=fs_dir_target
            ),
            select_feature_by_nonlinear_correlation(
                X_numerical, y, target_type, percentile, save_dir=fs_dir_target
            ),
            select_feature_by_mi(
                X_numerical, y, target_type, percentile, save_dir=fs_dir_target
            ),
            select_feature_by_feat_imp(
                X_numerical, y, target_type, percentile, save_dir=fs_dir_target
            ),
            select_feature_by_rfe(
                X_numerical, y, target_type, percentile, save_dir=fs_dir_target
            ),
            # select_feature_by_sfs(
            #     X_numerical, y, target_type, percentile, save_dir=fs_dir_target
            # ), # TODO: this is taking too long
        ]
    else:
        # Use ProcessPoolExecutor to run tasks in parallel
        with ProcessPoolExecutor() as executor:
            # Submit different functions to be executed in parallel
            futures = [
                executor.submit(
                    select_feature_by_linear_correlation,
                    X_numerical,
                    y,
                    target_type,
                    percentile,
                    save_dir=fs_dir_target,
                ),
                executor.submit(
                    select_feature_by_nonlinear_correlation,
                    X_numerical,
                    y,
                    target_type,
                    percentile,
                    save_dir=fs_dir_target,
                ),
                executor.submit(
                    select_feature_by_mi,
                    X_numerical,
                    y,
                    target_type,
                    percentile,
                    save_dir=fs_dir_target,
                ),
                executor.submit(
                    select_feature_by_feat_imp,
                    X_numerical,
                    y,
                    target_type,
                    percentile,
                    save_dir=fs_dir_target,
                ),
                executor.submit(
                    select_feature_by_rfe,
                    X_numerical,
                    y,
                    target_type,
                    percentile,
                    save_dir=fs_dir_target,
                ),
                executor.submit(
                    select_feature_by_sfs,
                    X_numerical,
                    y,
                    target_type,
                    percentile,
                    save_dir=fs_dir_target,
                ),
            ]

            # Wait for all futures to complete and gather the results
            with tqdm(total=len(futures)) as pbar:
                for future in as_completed(futures):
                    results.append(future.result())
                    pbar.update(1)
    logger.info(f"Finished feature selection for target {target_number}")

    stop = time.time()

    # Once all tasks are completed, start by inserting results to db
    feat_scores = pd.concat(
        results,
        axis=0,
    )

    logger.info("Inserting feature selection results to db...")
    rows = []

    with get_db() as db:
        feature_map = {f.name: f.id for f in Feature.get_all(db=db, limit=20000)}
        for row in feat_scores.itertuples(index=False):
            feature_id = feature_map.get(row.features)
            if not feature_id:
                continue  # or raise if feature must exist

            rows.append(
                {
                    "feature_selection_id": feature_selection.id,
                    "feature_id": feature_id,
                    "method": row.method,
                    "score": row.score,
                    "pvalue": None if pd.isna(row.pvalue) else row.pvalue,
                    "support": row.support,
                    "rank": row.rank,
                    "training_time": row.training_time,
                }
            )

        if len(rows) == 0:
            raise ValueError(f"No features selected for TARGET_{target_number}")

        FeatureSelectionRank.bulk_upsert(rows=rows, db=db)

    # Merge the results
    features_selected = feat_scores[feat_scores["support"] == True][
        ["features", "rank"]
    ]
    features_selected.sort_values("rank", inplace=True)
    features_selected.drop_duplicates("features", inplace=True)

    features_selected_list = features_selected["features"].values.tolist()

    logger.info("Merging feature selection methods...")
    # features_selected = list(dict.fromkeys(features_selected_by_mi + features_selected_by_nonlinear_correlation + features_selected_by_linear_correlation))
    features_selected_by_every_methods = set(results[0]["features"].values.tolist())

    for df in results[1:]:
        features_selected_by_every_methods &= set(
            df["features"].values.tolist()
        )  # intersection

    features_selected_by_every_methods = list(features_selected_by_every_methods)

    logger.debug(
        f"We selected {len(features_selected_list)} features and {len(features_selected_by_every_methods)} were selected unanimously:"
    )
    logger.debug(features_selected_by_every_methods)

    pd.Series(features_selected_list).to_csv(
        f"{fs_dir_target}/features_before_corr.csv",
        index=True,
        header=True,
        index_label="ID",
    )
    features, features_correlated = remove_correlated_features(
        X, features_selected_list, corr_threshold
    )
    pd.Series(features).to_csv(
        f"{fs_dir_target}/features_before_max.csv",
        index=True,
        header=True,
        index_label="ID",
    )
    features = features[:max_features]

    features += categorical_features_selected if target_type == "classification" else []
    logger.debug(
        f"Final pre-selection: {len(features)} features below {corr_threshold}% out of {len(features_selected_list)} features, and rejected {len(features_correlated)} features, {100*len(features)/len(features_selected_list):.2f}% features selected"
    )

    features_selected_by_every_methods_uncorrelated = list(
        set(features) & set(features_selected_by_every_methods)
    )
    logger.debug(
        f"In this pre-selection, there is {len(features_selected_by_every_methods_uncorrelated)} features from the {len(features_selected_by_every_methods)} selected unanimously\n"
    )

    logger.debug(
        features_selected[features_selected["features"].isin(features)].to_markdown()
    )

    best_features_path = Path(
        f"{preprocessing_dir}/features_{target_number}.pkl"
    ).resolve()
    if PYTHON_ENV != "Test":
        joblib.dump(features, best_features_path)

    db_features = Feature.filter(name__in=features)
    # Order matters, to keep the same order in db as in features, we need: map features by name
    feature_by_name = {f.name: f for f in db_features}
    # Reorder them according to original `features` list
    ordered_db_features = [
        feature_by_name[name] for name in features if name in feature_by_name
    ]

    feature_selection = FeatureSelection.get(feature_selection.id)
    feature_selection = feature_selection.add_features(ordered_db_features)
    feature_selection.training_time = stop - start
    feature_selection.best_features_path = best_features_path
    feature_selection.save()

    return features


# TODO : can we use this to select the ideal number of features ?
def feature_selection_analysis(feature_selection_id: int, n_components: int = 5):

    feature_selection = FeatureSelection.get(feature_selection_id)
    dataset_dir = feature_selection.dataset.path
    features = [f.name for f in feature_selection.features]
    target = feature_selection.target.name
    target_number = target.split("_")[1]

    train, val, train_scaled, val_scaled, _scaler_y = load_train_data(
        dataset_dir, target_number, target_type=feature_selection.target.type
    )
    train = train[features + [target]]
    train_scaled = train_scaled[features + [target]]

    logger.info("Plot features correlation with target variable...")

    correlations = train.corr()[target].sort_values(ascending=False)

    plt.figure(figsize=(12, 6))
    sns.barplot(x=correlations.index, y=correlations.values, palette="coolwarm")
    plt.xticks(rotation=90)
    plt.title("Feature correlation with target variable")
    plt.ylabel("Correlation")
    plt.xlabel("Features")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    plt.figure(figsize=(14, 10))
    sns.heatmap(train.corr(), annot=True, fmt=".2f", cmap="coolwarm", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.show()

    logger.info("Plot explained variance by components...")
    n_components = min(len(features), n_components)
    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(train_scaled)

    explained_variance = pca.explained_variance_ratio_

    plt.figure(figsize=(10, 7))
    plt.bar(
        range(1, len(explained_variance) + 1),
        explained_variance,
        label="Explained Variance",
    )
    plt.plot(
        range(1, len(explained_variance) + 1),
        np.cumsum(explained_variance),
        label="Cumulative Explained Variance",
        color="orange",
        marker="o",
    )
    plt.title("Explained Variance by Components")
    plt.xlabel("Number of Components")
    plt.ylabel("Explained Variance")
    plt.legend()
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    logger.info("Main PCA vs target variable...")
    plt.scatter(
        X_pca[:, 0],
        X_pca[:, 1],
        c=train[target],
        cmap="coolwarm",
        alpha=0.7,
    )
    plt.title("PCA of target variable")
    plt.xlabel("First Principal Component")
    plt.ylabel("Second Principal Component")
    plt.colorbar()
    plt.show()


# scaling
def scale_data(
    df: pd.DataFrame, save_dir: str, scaler_x=None, scalers_y: Optional[list] = None
):
    logger.info("Scale data...")
    X = df.loc[:, ~df.columns.str.contains("^TARGET_")]

    if scaler_x:
        X_scaled = pd.DataFrame(
            scaler_x.transform(X), columns=list(X.columns), index=X.index
        )
    else:
        scaler_x = StandardScaler()  # MinMaxScaler(feature_range=(-1,1))
        X_scaled = pd.DataFrame(
            scaler_x.fit_transform(X), columns=list(X.columns), index=X.index
        )
        if PYTHON_ENV != "Test":
            joblib.dump(scaler_x, f"{save_dir}/scaler_x.pkl")

    # Determine which targets need to be scaled
    targets_numbers_to_scale = [i for i in TARGETS_NUMBER if i not in TARGETS_CLF]

    # Dictionary to store scaled target data
    scaled_targets = {}

    if scalers_y:
        for target_number in targets_numbers_to_scale:
            y = df[[f"TARGET_{target_number}"]]
            scaled_targets[target_number] = pd.DataFrame(
                scalers_y[f"scaler_y_{target_number}"].transform(y.values),
                columns=y.columns,
                index=y.index,
            )
    else:
        scalers_y = {}
        for target_number in targets_numbers_to_scale:
            scaler_y = StandardScaler()
            y = df[[f"TARGET_{target_number}"]]

            scaled_y = pd.DataFrame(
                scaler_y.fit_transform(y.values),
                columns=y.columns,
                index=y.index,
            )
            if PYTHON_ENV != "Test":
                joblib.dump(scaler_y, f"{save_dir}/scaler_y_{target_number}.pkl")

            scalers_y[f"scaler_y_{target_number}"] = scaler_y
            scaled_targets[target_number] = scaled_y

    # Reconstruct y_scaled in the original order
    y_scaled = pd.concat(
        [scaled_targets[target_number] for target_number in targets_numbers_to_scale],
        axis=1,
    )
    y_not_scaled = df[df.columns.intersection([f"TARGET_{i}" for i in TARGETS_CLF])]

    # Ensure the final DataFrame keeps the original order
    df_scaled = pd.concat(
        [X_scaled, y_scaled, y_not_scaled],
        axis=1,
    )[
        df.columns
    ]  # Reorder columns to match original `df`

    if not df_scaled.columns.equals(df.columns):
        raise Exception("Columns are not in the same order after scaling.")

    return df_scaled, scaler_x, scalers_y


# Reshape into 3D tensors for recurrent models
def reshape_time_series(
    train: pd.DataFrame,
    val: pd.DataFrame,
    test: pd.DataFrame,
    features: list,
    timesteps: int = 120,
):
    # always scale for recurrent layers : train should be scaled

    target_columns = train.columns.intersection([f"TARGET_{i}" for i in TARGETS_NUMBER])

    data = pd.concat([train, val, test], axis=0)

    data_reshaped = reshape_df(data[features], data[GROUPING_COLUMN], timesteps)

    data_reshaped[target_columns] = data[target_columns]

    logger.info("Separating train, val, test data and creating np arrays...")
    train_reshaped = data_reshaped.loc[train.index]
    val_reshaped = data_reshaped.loc[val.index]
    test_reshaped = data_reshaped.loc[test.index]

    x_train_reshaped = np.array(train_reshaped["RECURRENT_FEATURES"].values.tolist())
    y_train_reshaped = np.array(train_reshaped[target_columns].reset_index())
    x_val_reshaped = np.array(val_reshaped["RECURRENT_FEATURES"].values.tolist())
    y_val_reshaped = np.array(val_reshaped[target_columns].reset_index())
    x_test_reshaped = np.array(test_reshaped["RECURRENT_FEATURES"].values.tolist())
    y_test_reshaped = np.array(test_reshaped[target_columns].reset_index())

    reshaped_data = {
        "x_train_reshaped": x_train_reshaped,
        "y_train_reshaped": y_train_reshaped,
        "x_val_reshaped": x_val_reshaped,
        "y_val_reshaped": y_val_reshaped,
        "x_test_reshaped": x_test_reshaped,
        "y_test_reshaped": y_test_reshaped,
    }

    return reshaped_data


def reshape_df(df: pd.DataFrame, stock_column: pd.DataFrame, timesteps: int):
    fill_value = [[[0] * len(df.columns)]]

    def shiftsum(x, timesteps: int):
        tmp = x.copy()
        for i in range(1, timesteps):
            tmp = x.shift(i, fill_value=fill_value) + tmp
        return tmp

    logger.info("Grouping each feature in a unique column with list...")
    df_reshaped = df.apply(list, axis=1).apply(lambda x: [list(x)])
    df_reshaped = pd.concat([df_reshaped, stock_column], axis=1)

    logger.info("Grouping method stock and creating timesteps...")
    df_reshaped = (
        df_reshaped.groupby(GROUPING_COLUMN)[0]
        .apply(lambda x: shiftsum(x, timesteps))
        .reset_index(GROUPING_COLUMN, drop=True)
        .rename("RECURRENT_FEATURES")
    )
    df_reshaped = pd.DataFrame(df_reshaped)

    return df_reshaped


def load_train_data(dataset_dir, target_number, target_type="regression"):
    train_data_dir = f"{dataset_dir}/data"
    preprocessing_dir = f"{dataset_dir}/preprocessing"

    _scaler_y = (
        joblib.load(f"{preprocessing_dir}/scaler_y_{target_number}.pkl")
        if target_type == "regression"
        else None
    )

    logger.info("Loading data...")
    train = joblib.load(f"{train_data_dir}/train.pkl")
    val = joblib.load(f"{train_data_dir}/val.pkl")
    train_scaled = joblib.load(f"{train_data_dir}/train_scaled.pkl")
    val_scaled = joblib.load(f"{train_data_dir}/val_scaled.pkl")

    return train, val, train_scaled, val_scaled, _scaler_y
