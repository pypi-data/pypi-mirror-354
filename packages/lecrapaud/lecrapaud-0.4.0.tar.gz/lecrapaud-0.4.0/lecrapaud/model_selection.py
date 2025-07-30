import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os
import json
import warnings
import joblib
import glob
from pathlib import Path

os.environ["COVERAGE_FILE"] = str(Path(".coverage").resolve())

# ML models
from sklearn.model_selection import TimeSeriesSplit
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    mean_absolute_percentage_error,
    root_mean_squared_error,
    mean_absolute_error,
    r2_score,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    log_loss,
    roc_auc_score,
    roc_curve,
    auc,
    precision_recall_curve,
    average_precision_score,
    confusion_matrix,
)
from sklearn.preprocessing import LabelBinarizer
import lightgbm as lgb
import xgboost as xgb

# DL models
import tensorflow as tf
import keras
from keras.callbacks import EarlyStopping, TensorBoard
from keras.metrics import (
    Precision,
    Recall,
    F1Score,
)
from keras.losses import BinaryCrossentropy, CategoricalCrossentropy
from keras.optimizers import Adam

K = tf.keras.backend
from tensorboardX import SummaryWriter

# Optimization
import ray
from ray.tune import Tuner, TuneConfig, with_parameters
from ray.train import RunConfig
from ray.tune.search.hyperopt import HyperOptSearch
from ray.tune.search.bayesopt import BayesOptSearch
from ray.tune.logger import TBXLoggerCallback
from ray.tune.schedulers import ASHAScheduler
from ray.air import session

# Internal library
from src.search_space import ml_models, dl_recurrent_models
from src.directory_management import clean_directory
from src.utils import copy_any, contains_best, logger, serialize_for_json
from src.config import PYTHON_ENV
from src.feature_selection import TARGETS_CLF, DATE_COLUMN, load_train_data
from src.db.models import Model, ModelSelection, ModelTraining, Score, Target, Dataset

# Reproducible result
keras.utils.set_random_seed(42)
np.random.seed(42)
tf.config.experimental.enable_op_determinism()


# test configuration
def test_hardware():
    devices = tf.config.list_physical_devices()
    logger.info("\nDevices: ", devices)

    gpus = tf.config.list_physical_devices("GPU")
    if gpus:
        details = tf.config.experimental.get_device_details(gpus[0])
        logger.info("GPU details: ", details)


# Suppress specific warning messages related to file system monitor
# logging.getLogger("ray").setLevel(logging.CRITICAL)
# logging.getLogger("ray.train").setLevel(logging.CRITICAL)
# logging.getLogger("ray.tune").setLevel(logging.CRITICAL)
# logging.getLogger("ray.autoscaler").setLevel(logging.CRITICAL)
# logging.getLogger("ray.raylet").setLevel(logging.CRITICAL)
# logging.getLogger("ray.monitor").setLevel(logging.CRITICAL)
# logging.getLogger("ray.dashboard").setLevel(logging.CRITICAL)
# logging.getLogger("ray.gcs_server").setLevel(logging.CRITICAL)

warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")


# Metrics
def rmse_tf(y_true, y_pred):
    y_true, y_pred = unscale_tf(y_true, y_pred)
    results = K.sqrt(K.mean(K.square(y_pred - y_true)))
    return results


def mae_tf(y_true, y_pred):
    y_true, y_pred = unscale_tf(y_true, y_pred)
    results = K.mean(K.abs(y_pred - y_true))
    return results


def unscale_tf(y_true, y_pred):
    if _target_type == "regression":
        scale = K.constant(_scaler_y.scale_[0])
        mean = K.constant(_scaler_y.mean_[0])

        y_true = K.mul(y_true, scale)
        y_true = K.bias_add(y_true, mean)

        y_pred = K.mul(y_pred, scale)
        y_pred = K.bias_add(y_pred, mean)
    return y_true, y_pred


def recall_tf(y_true, y_pred):
    y_true = K.ones_like(y_true)
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    all_positives = K.sum(K.round(K.clip(y_true, 0, 1)))

    recall = true_positives / (all_positives + K.epsilon())
    return recall


def precision_tf(y_true, y_pred):
    y_true = K.ones_like(y_true)
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))

    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_score_tf(y_true, y_pred):
    precision = precision_tf(y_true, y_pred)
    recall = recall_tf(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))


def get_log_dir(training_target_dir: str, model_name="test_model"):
    """Generates a structured log directory path for TensorBoard."""
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_dir = (
        Path(training_target_dir + "/tensorboard") / model_name / f"run_{timestamp}"
    )
    log_dir.mkdir(parents=True, exist_ok=True)  # Create directories if they don't exist
    return str(log_dir)


# Functions to fit & evaluate models
def fit_sklearn(x_train, y_train, x_val, y_val, create_model, params, config):

    # Create & Compile the model
    model = create_model(**params)

    # Train the model
    logger.info("Fitting the model...")
    logger.info(f"x_train shape: {x_train.shape}, x_val shape: {x_val.shape}")
    logger.info(f"y_train shape: {y_train.shape}, y_val shape: {y_val.shape}")

    model.fit(x_train, y_train)

    if (
        _target_type == "classification"
        and "loss" in model.get_params().keys()
        and "hinge" in model.get_params()["loss"]
    ):
        # This is for SVC models with hinge loss
        # You should use CalibratedClassifierCV when you are working with classifiers that do not natively output well-calibrated probability estimates.
        # TODO: investigate if we should use calibration for random forest, gradiant boosting models, and bagging models
        logger.info(
            f"Re-Calibrating {config["model_name"]} to get predict probabilities..."
        )
        calibrator = CalibratedClassifierCV(model, cv="prefit", n_jobs=-1)
        model = calibrator.fit(x_train, y_train)

    # set model_name after calibrator
    model.model_name = config["model_name"]

    logger.info(f"Successfully created a {model.model_name} at {datetime.now()}")

    return model


def fit_boosting(x_train, y_train, x_val, y_val, create_model, params, config):
    """
    This is using lightGBM or XGboost C++ librairies
    """
    lightGBM = create_model == "lgb"

    # Datasets
    Dataset = lgb.Dataset if lightGBM else xgb.DMatrix
    train_data = Dataset(x_train, label=y_train)
    val_data = Dataset(x_val, label=y_val)

    # Callbacks
    log_dir = get_log_dir(_training_target_dir, create_model)

    # Create a TensorBoardX writer
    writer = SummaryWriter(log_dir)
    evals_result = {}

    # Training
    labels = np.unique(y_train)
    num_class = (
        labels.size if _target_type == "classification" and labels.size > 2 else 1
    )
    logger.info("Fitting the model...")
    logger.info(f"x_train shape: {x_train.shape}, x_val shape: {x_val.shape}")
    logger.info(f"y_train shape: {y_train.shape}, y_val shape: {y_val.shape}")

    if lightGBM:

        def tensorboard_callback(env):
            for i, metric in enumerate(env.evaluation_result_list):
                metric_name, _, metric_value, _ = metric
                writer.add_scalar(
                    f"LightGBM/{metric_name}", metric_value, env.iteration
                )

        loss = (
            "regression"
            if _target_type == "regression"
            else ("binary" if num_class <= 2 else "multiclass")
        )
        eval_metric = (
            "rmse"
            if _target_type == "regression"
            else ("binary_logloss" if num_class <= 2 else "multi_logloss")
        )
        model = lgb.train(
            params={
                **params["model_params"],
                "objective": loss,
                "metric": eval_metric,
                "num_class": num_class,
            },
            num_boost_round=params["num_boost_round"],
            train_set=train_data,
            valid_sets=[train_data, val_data],
            valid_names=["train", "val"],
            callbacks=[
                lgb.early_stopping(stopping_rounds=params["early_stopping_rounds"]),
                lgb.record_evaluation(evals_result),
                tensorboard_callback,
            ],
        )
    else:

        class TensorBoardCallback(xgb.callback.TrainingCallback):

            def __init__(self, log_dir: str):
                self.writer = SummaryWriter(log_dir=log_dir)

            def after_iteration(
                self,
                model,
                epoch: int,
                evals_log: xgb.callback.TrainingCallback.EvalsLog,
            ) -> bool:
                if not evals_log:
                    return False

                for data, metric in evals_log.items():
                    for metric_name, log in metric.items():
                        score = log[-1][0] if isinstance(log[-1], tuple) else log[-1]
                        self.writer.add_scalar(f"XGBoost/{data}", score, epoch)

                return False

        tensorboard_callback = TensorBoardCallback(log_dir)

        loss = (
            "reg:squarederror"
            if _target_type == "regression"
            else ("binary:logistic" if num_class <= 2 else "multi:softprob")
        )
        eval_metric = (
            "rmse"
            if _target_type == "regression"
            else ("logloss" if num_class <= 2 else "mlogloss")
        )
        model = xgb.train(
            params={
                **params["model_params"],
                "objective": loss,
                "eval_metric": eval_metric,
                "num_class": num_class,
            },
            num_boost_round=params["num_boost_round"],
            dtrain=train_data,
            evals=[(val_data, "val"), (train_data, "train")],
            callbacks=[
                xgb.callback.EarlyStopping(
                    rounds=params["early_stopping_rounds"], save_best=True
                ),
                xgb.callback.EvaluationMonitor(),  # This shows evaluation results at each iteration
                tensorboard_callback,
            ],
            evals_result=evals_result,  # Record evaluation result
            verbose_eval=0,
        )

    model.model_name = create_model
    logger.info(f"Successfully created a {model.model_name} at {datetime.now()}")

    # Close the writer after training is done
    writer.close()

    if _plot:
        # Plot loss per epoch
        train_loss = evals_result["train"][eval_metric]
        val_loss = evals_result["val"][eval_metric]
        logs = pd.DataFrame({"train": train_loss, "val": val_loss})

        plt.figure(figsize=(14, 4))
        plt.plot(logs.loc[:, "train"], lw=2, label="Training loss")
        plt.plot(logs.loc[:, "val"], lw=2, label="Validation loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        plt.show()

    return model


def fit_recurrent(x_train, y_train, x_val, y_val, create_model, params, config):

    # Create the model
    labels = np.unique(y_train[:, 0])
    num_class = labels.size if _target_type == "classification" else None
    input_shape = (x_train.shape[1], x_train.shape[2])
    model = create_model(params, input_shape, _target_type, num_class)

    # Compile the model
    loss = (
        rmse_tf
        if _target_type == "regression"
        else (
            BinaryCrossentropy(from_logits=False)
            if num_class <= 2
            else CategoricalCrossentropy(from_logits=False)
        )
    )
    optimizer = Adam(learning_rate=params["learning_rate"], clipnorm=params["clipnorm"])
    metrics = (
        [mae_tf]
        if _target_type == "regression"
        else (
            ["accuracy", Precision(), Recall()]
            if num_class <= 2
            else ["categorical_accuracy"]
        )
    )
    model.compile(optimizer=optimizer, loss=loss, metrics=metrics)

    # Callbacks
    log_dir = get_log_dir(_training_target_dir, model.model_name)

    tensorboard_callback = TensorBoard(log_dir=log_dir)
    early_stopping_callback = EarlyStopping(
        monitor="val_loss", patience=3, restore_best_weights=True, start_from_epoch=5
    )

    # Custom callbacks
    class PrintTrainableWeights(keras.callbacks.Callback):
        def on_epoch_end(self, epoch, logs={}):
            logger.info(model.trainable_variables)

    class GradientCalcCallback(keras.callbacks.Callback):
        def __init__(self):
            self.epoch_gradient = []

        def get_gradient_func(self, model):
            # grads = K.gradients(model.total_loss, model.trainable_weights)
            grads = K.gradients(model.loss, model.trainable_weights)
            # inputs = model.model.inputs + model.targets + model.sample_weights
            # use below line of code if above line doesn't work for you
            # inputs = model.model._feed_inputs + model.model._feed_targets + model.model._feed_sample_weights
            inputs = (
                model._feed_inputs + model._feed_targets + model._feed_sample_weights
            )
            func = K.function(inputs, grads)
            return func

    def on_epoch_end(self, epoch, logs=None):
        get_gradient = self.get_gradient_func(model)
        grads = get_gradient([x_val, y_val[:, 0], np.ones(len(y_val[:, 0]))])
        self.epoch_gradient.append(grads)

    # Train the model
    if _target_type == "classification" and num_class > 2:
        lb = LabelBinarizer(sparse_output=False)  # Change to True for sparse matrix
        lb.fit(labels)
        y_train = lb.transform(y_train[:, 0].flatten())
        y_val = lb.transform(y_val[:, 0].flatten())
    else:
        y_train = y_train[:, 0].flatten()
        y_val = y_val[:, 0].flatten()

    logger.info("Fitting the model...")
    logger.info(f"x_train shape: {x_train.shape}, x_val shape: {x_val.shape}")
    logger.info(f"y_train shape: {y_train.shape}, y_val shape: {y_val.shape}")

    history = model.fit(
        x_train,
        y_train,
        batch_size=params["batch_size"],
        verbose=0,
        epochs=params["epochs"],
        shuffle=False,
        validation_data=(x_val, y_val),
        callbacks=[early_stopping_callback, tensorboard_callback],
    )

    logger.info(f"Successfully created a {model.model_name} at {datetime.now()}")
    # logger.info(pd.DataFrame(gradiant.epoch_gradient))

    if _plot:
        # Plot loss per epoch
        logs = pd.DataFrame(history.history)

        plt.figure(figsize=(14, 4))
        plt.plot(logs.loc[:, "loss"], lw=2, label="Training loss")
        plt.plot(logs.loc[:, "val_loss"], lw=2, label="Validation loss")
        plt.xlabel("Epoch")
        plt.ylabel("Loss")
        plt.legend()
        plt.show()

    return model


def predict(
    model, data: pd.DataFrame, target_type: str, config: dict, threshold: float = 0.5
):
    """Function to get prediction from model. Support sklearn, keras and boosting models such as xgboost and lgboost

    Args:
        - model: the train model to predict value
        - data: the data for prediction
        - target_type: classification or regression
        - config: dict containing model config
    """
    if config["recurrent"] or model.model_name in ["lgb", "xgb"]:
        # keras, lgb & xgb
        if model.model_name == "lgb":
            # Direct prediction for LightGBM
            pred = model.predict(data)
        elif model.model_name == "xgb":
            # Convert val_data to DMatrix for XGBoost
            d_data = xgb.DMatrix(data)
            pred = model.predict(d_data)
        else:
            # Reshape (flatten) for keras if not multiclass
            pred = model.predict(data)
            if pred.shape[1] == 1:
                pred = pred.reshape(-1)

        if target_type == "classification":
            num_class = pred.shape[1] if len(pred.shape) > 1 else 2

            if num_class <= 2:
                # For binary classification, concatenate the predicted probabilities for both classes
                pred_df = pd.DataFrame(
                    {
                        0: 1 - pred,  # Probability of class 0
                        1: pred,  # Probability of class 1
                    },
                )
            else:
                # For multi-class classification, use the predicted probabilities for each class
                pred_df = pd.DataFrame(pred, columns=range(num_class))

            # Get final predictions (argmax for multi-class, threshold for binary)
            if num_class == 2:
                pred_df["PRED"] = np.where(
                    pred_df[1] >= threshold, 1, 0
                )  # Class 1 if prob >= threshold
            else:
                pred_df["PRED"] = pred_df.idxmax(
                    axis=1
                )  # Class with highest probability for multiclasses

            # Reorder columns to show predicted class first, then probabilities
            pred = pred_df[["PRED"] + list(range(num_class))]

        else:
            pred = pd.Series(pred, name="PRED")

        # set index for lgb and xgb (for keras, as we use np array, we need to set index outside)
        if model.model_name in ["lgb", "xgb"]:
            pred.index = data.index
    else:
        # sk learn
        pred = pd.Series(model.predict(data), index=data.index, name="PRED")
        if target_type == "classification":
            pred_proba = pd.DataFrame(
                model.predict_proba(data),
                index=data.index,
                columns=[
                    int(c) if isinstance(c, float) and c.is_integer() else c
                    for c in model.classes_
                ],
            )

            # Apply threshold for binary classification
            if len(model.classes_) == 2:
                positive_class = model.classes_[1]  # Assuming classes are ordered
                pred = (pred_proba[positive_class] >= threshold).astype(int)
                pred.name = "PRED"

            pred = pd.concat([pred, pred_proba], axis=1)

    return pred


def evaluate(prediction: pd.DataFrame, target_type: str):
    """
    Function to evaluate model performance

    Args:
        - prediction: the prediction dataframe containing TARGET and PRED columns, as well as predicted probablities for each class for classification tasks
        - target_type: classification or regression
    """
    score = {}
    y_true = prediction["TARGET"]
    y_pred = prediction["PRED"]

    if target_type == "regression":
        # Main metrics
        score["RMSE"] = root_mean_squared_error(y_true, y_pred)
        score["MAE"] = mean_absolute_error(y_true, y_pred)
        score["MAPE"] = mean_absolute_percentage_error(y_true, y_pred)
        score["R2"] = r2_score(y_true, y_pred)

        # Robustness: avoid division by zero
        std_target = y_true.std()
        mean_target = y_true.mean()
        median_target = y_true.median()

        # RMSE / STD
        score["RMSE_STD_RATIO"] = (
            float(100 * score["RMSE"] / std_target) if std_target else 1000
        )

        # Median absolute deviation (MAD)
        mam = (y_true - mean_target).abs().median()  # Median Abs around Mean
        mad = (y_true - median_target).abs().median()  # Median Abs around Median
        score["MAM"] = mam
        score["MAD"] = mad
        score["MAE_MAM_RATIO"] = (
            float(100 * score["MAE"] / mam) if mam else 1000
        )  # MAE / MAD → Plus stable, moins sensible aux outliers.
        score["MAE_MAD_RATIO"] = (
            float(100 * score["MAE"] / mad) if mad else 1000
        )  # MAE / Médiane des écarts absolus autour de la moyenne: Moins robuste aux outliers

    else:

        labels = np.unique(y_true)
        num_classes = labels.size
        y_pred_proba = (
            prediction[1] if num_classes == 2 else prediction.iloc[:, 2:].values
        )
        if num_classes > 2:
            lb = LabelBinarizer(sparse_output=False)  # Change to True for sparse matrix
            lb.fit(labels)
            y_true_onhot = lb.transform(y_true)
            y_pred_onehot = lb.transform(y_pred)

        score["LOGLOSS"] = log_loss(y_true, y_pred_proba)
        score["ACCURACY"] = accuracy_score(y_true, y_pred)
        score["PRECISION"] = precision_score(
            y_true,
            y_pred,
            average=("binary" if num_classes == 2 else "macro"),
        )
        score["RECALL"] = recall_score(
            y_true,
            y_pred,
            average=("binary" if num_classes == 2 else "macro"),
        )
        score["F1"] = f1_score(
            y_true,
            y_pred,
            average=("binary" if num_classes == 2 else "macro"),
        )
        score["ROC_AUC"] = float(roc_auc_score(y_true, y_pred_proba, multi_class="ovr"))
        (
            score["THRESHOLD"],
            score["PRECISION_AT_THRESHOLD"],
            score["RECALL_AT_THRESHOLD"],
        ) = (
            find_best_precision_threshold(prediction)
            if num_classes == 2
            else (None, None, None)
        )
    return score


def train_model(params, x_train, y_train, x_val, y_val, config):
    if "_type_name" in config.keys() and config["_type_name"] == "hyperopts":
        global _target_number
        global _target_type
        global _session_name
        global _plot
        global _type_name
        global _scaler_y
        global _training_target_dir
        _target_number = config["_target_number"]
        _target_type = config["_target_type"]
        _session_name = config["_session_name"]
        _plot = config["_plot"]
        _type_name = config["_type_name"]
        _scaler_y = config["_scaler_y"]
        _training_target_dir = config["_training_target_dir"]

        # warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
        # logging.getLogger("ray").setLevel(logging.CRITICAL)
        # logging.getLogger("ray.tune").setLevel(logging.CRITICAL)
        # logging.getLogger("ray.raylet").setLevel(logging.CRITICAL)
        # logging.getLogger("raylet").setLevel(logging.CRITICAL)

    logger.info(
        f"TARGET_{_target_number} - Training a {config['model_name']} at {datetime.now()} : {_session_name}, TARGET_{_target_number}"
    )

    recurrent = config["recurrent"]
    create_model = config["create_model"]

    if recurrent:
        timesteps = params["timesteps"]
        x_train = x_train[:, -timesteps:, :]
        x_val = x_val[:, -timesteps:, :]

    # Compile and fit model on train set
    start = time.time()
    if recurrent:
        fit = fit_recurrent
    elif (create_model == "lgb") or (create_model == "xgb"):
        fit = fit_boosting
    else:
        fit = fit_sklearn
    model = fit(
        x_train,
        y_train,
        x_val,
        y_val,
        create_model,
        params=params,
        config=config,
    )
    stop = time.time()

    # Prediction on val set
    y_pred = predict(model, x_val, _target_type, config)

    # fix for recurrent model because x_val has no index as it is a 3D np array
    if config["recurrent"]:
        y_val = pd.DataFrame(y_val, columns=["TARGET", "index"]).set_index("index")
        y_pred.index = y_val.index

    prediction = pd.concat([y_val, y_pred], axis=1)

    # Unscale the data
    if config["need_scaling"] and _target_type == "regression":
        # scaler_y needs 2D array with shape (-1, 1)
        prediction.loc[:, "TARGET"] = _scaler_y.inverse_transform(
            prediction[["TARGET"]].values
        )
        prediction.loc[:, "PRED"] = _scaler_y.inverse_transform(
            prediction[["PRED"]].values
        )

    # Evaluate model
    score = {
        "DATE": datetime.now(),
        "SESSION": _session_name,
        "TRAIN_DATA": x_train.shape[0],
        "VAL_DATA": x_val.shape[0],
        "FEATURES": x_train.shape[-1],
        "MODEL_NAME": model.model_name,
        "TYPE": _type_name,
        "TRAINING_TIME": stop - start,
        "EVAL_DATA_STD": prediction["TARGET"].std(),
    }

    score.update(evaluate(prediction, _target_type))

    if _type_name == "hyperopts":
        session.report(metrics=score)
        ray.tune.report(metrics=score)
        return score

    return score, model, prediction


# Main training function
def model_selection(
    dataset_id: int,
    models_idx: list,
    target_number: int,
    session_name,
    perform_hyperoptimization=True,
    perform_crossval=False,
    number_of_trials=20,
    plot=True,
    clean_dir=False,  # TODO: This has been unused because now feature_selection is in the target directory
    preserve_model=True,
    reshaped_data=None,
    data=None,
):
    """
    Selects the best models based on a target variable, optionally performing hyperparameter optimization
    and cross-validation, and manages outputs in a session-specific directory.

    Args:
        models_idx (list):
            A list of indices or identifiers representing the models to evaluate.
            Each identifier corresponds to a predefined or available model.

        target_number (int):
            The number of the target variable (e.g., column index or predefined target) to predict.
            This determines the dataset's output variable for training and evaluation.

        session_name (str):
            A name for the current session, used to organize and store results
            (e.g., logs, metrics, trained models) in a session-specific directory.

        perform_hyperoptimization (bool, optional):
            Whether to perform hyperparameter optimization for the models.
            If `True`, the function will attempt to tune the hyperparameters of each model.
            Defaults to `True`.

        perform_crossval (bool, optional):
            Whether to perform cross-validation to evaluate model performance.
            If `True`, the function will use cross-validation to compute metrics.
            Defaults to `True`.

        number_of_trials (int, optional):
            The number of trials to run for hyperparameter optimization.
            Ignored if `perform_hyperoptimization` is `False`.
            Defaults to `20`.

        plot (bool, optional):
            Whether to enable plotting during the process.
            If `True`, plot will be displayed.
            Defaults to `True`.

        clean_dir (bool, optional):
            Whether to clean the entire target training directory before starting the process.
            If `True`, any existing files in the target training directory will be removed.
            Defaults to `False`.

        preserve_model (bool, optional):
            Whether to run the search even if there is already a best model in the directory.
            If `False`, previous best models won't be erased and the search will be skipped.
            Defaults to `False`.

    Returns:
        None
        The function runs the model selection process and outputs results
        (e.g., logs, metrics, and optionally models) to the session directory.
    """
    global _target_number
    global _target_type
    global _session_name
    global _plot
    global _type_name
    global _scaler_y
    global _training_target_dir

    global_vars = [
        "_target_number",
        "_target_type",
        "_session_name",
        "_plot",
        "_type_name",
        "_scaler_y",
        "_training_target_dir",
    ]

    _target_number = target_number
    _target_type = "classification" if target_number in TARGETS_CLF else "regression"
    _session_name = session_name
    _plot = plot

    if dataset_id is None:
        raise ValueError("dataset_id is not provided.")

    dataset = Dataset.get(dataset_id)
    dataset_dir = dataset.path

    training_target_dir = f"{dataset_dir}/TARGET_{_target_number}"
    _training_target_dir = training_target_dir

    metric = "RMSE" if _target_type == "regression" else "LOGLOSS"

    # load features, scalers and data
    features = dataset.get_features(target_number)
    all_features = dataset.get_all_features()

    if data:
        train = data["train"]
        val = data["val"]
        train_scaled = data["train_scaled"]
        val_scaled = data["val_scaled"]
        _scaler_y = (
            data["scalers_y"][f"scaler_y_{target_number}"]
            if _target_type == "regression"
            else None
        )
    else:
        train, val, train_scaled, val_scaled, _scaler_y = load_train_data(
            dataset_dir, target_number, _target_type
        )

    list_models = ml_models + dl_recurrent_models

    if any(list_models[i].get("recurrent") for i in models_idx):
        if reshaped_data is None:
            raise ValueError("reshaped_data is not provided.")

        logger.info("Loading reshaped data...")
        x_train_reshaped = reshaped_data["x_train_reshaped"]
        y_train_reshaped = reshaped_data["y_train_reshaped"]
        x_val_reshaped = reshaped_data["x_val_reshaped"]
        y_val_reshaped = reshaped_data["y_val_reshaped"]

    # create model selection in db
    target = Target.find_by(name=f"TARGET_{target_number}")
    model_selection = ModelSelection.upsert(
        match_fields=["target_id", "dataset_id"],
        target_id=target.id,
        dataset_id=dataset.id,
    )

    # recurrent models starts at 9 # len(list_models)
    for i in models_idx:
        config = list_models[i]
        if config["recurrent"] is False and config[_target_type] is None:
            continue  # for naive bayes models that cannot be used in regression

        results_dir = f"{training_target_dir}/{config['model_name']}"
        if not os.path.exists(f"{results_dir}"):
            os.makedirs(f"{results_dir}")
        elif preserve_model and contains_best(results_dir):
            continue
        elif perform_hyperoptimization:
            clean_directory(results_dir)

        logger.info(f"Training a {config['model_name']}")
        model = Model.upsert(
            match_fields=["name", "type"],
            name=config["model_name"],
            type=_target_type,
        )
        model_training = ModelTraining.upsert(
            match_fields=["model_id", "model_selection_id"],
            model_id=model.id,
            model_selection_id=model_selection.id,
        )

        # getting data
        if config["recurrent"]:
            # Clear cluster from previous Keras session graphs.
            K.clear_session()

            features_idx = [i for i, e in enumerate(all_features) if e in set(features)]
            # TODO: Verify that features_idx are the right one, because scaling can re-arrange columns...
            x_train = x_train_reshaped[:, :, features_idx]
            y_train = y_train_reshaped[:, [target_number, 0]]
            x_val = x_val_reshaped[:, :, features_idx]
            y_val = y_val_reshaped[:, [target_number, 0]]
        else:
            new_config = config[_target_type]
            new_config["model_name"] = config["model_name"]
            new_config["recurrent"] = config["recurrent"]
            new_config["need_scaling"] = config["need_scaling"]
            config = new_config

            if config["need_scaling"] and _target_type == "regression":
                x_train = train_scaled[features]
                y_train = train_scaled[f"TARGET_{target_number}"].rename("TARGET")
                x_val = val_scaled[features]
                y_val = val_scaled[f"TARGET_{target_number}"].rename("TARGET")
            else:
                x_train = train[features]
                y_train = train[f"TARGET_{target_number}"].rename("TARGET")
                x_val = val[features]
                y_val = val[f"TARGET_{target_number}"].rename("TARGET")

        start = time.time()
        # Tuning hyperparameters
        if perform_hyperoptimization:
            _type_name = "hyperopts"

            for var in global_vars:
                config[var] = globals()[var]

            logger.info("Start tuning hyperparameters...")

            storage_path = f"{results_dir}/ray_results"
            # ray.shutdown()
            # ray.init(
            #     runtime_env={
            #         "working_dir": ".",  # or your project path
            #         "env_vars": {"PYTHONPATH": "."}
            #     }
            # )
            tuner = Tuner(
                trainable=with_parameters(
                    train_model,
                    x_train=x_train,
                    y_train=y_train,
                    x_val=x_val,
                    y_val=y_val,
                    config=config,
                ),
                param_space=config["search_params"],
                tune_config=TuneConfig(
                    metric=metric,
                    mode="min",
                    search_alg=HyperOptSearch(),
                    num_samples=number_of_trials,
                    scheduler=ASHAScheduler(max_t=100, grace_period=10),
                ),
                run_config=RunConfig(
                    stop={"training_iteration": 100},
                    storage_path=storage_path,
                    # name=datetime.now().strftime("%d-%m-%Y") + "-" + session_name,
                    callbacks=[TBXLoggerCallback()],
                    # log_to_file=("stdout.log", "stderr.log"), # depreciated
                    # verbose=0,
                ),
            )
            try:
                results = tuner.fit()

                best_result = results.get_best_result(metric, "max")
                best_params = best_result.config
                best_score = best_result.metrics

                # log results
                logger.info(f"Best hyperparameters found were:\n{best_params}")
                logger.info(f"Best Scores found were:\n{best_score}")

                df_results = results.get_dataframe()
                logger.info(
                    f"Markdown table with all trials :\n{df_results.to_markdown()}"
                )

                # save best params
                best_params_file = f"{training_target_dir}/best_params.json"
                try:
                    with open(best_params_file, "r") as f:
                        json_dict = json.load(f)
                except FileNotFoundError:
                    json_dict = {}

                json_dict[config["model_name"]] = serialize_for_json(best_params)
                with open(best_params_file, "w") as f:
                    json.dump(json_dict, f, indent=4)

            except Exception as e:
                ray.shutdown()
                raise Exception(e)
                logger.error(e)

            ray.shutdown()

            # Collect errors in single file
            collect_error_logs(
                training_target_dir=training_target_dir, storage_path=storage_path
            )

            # Clean up
            for var in global_vars:
                del config[var]
        else:
            try:
                with open(f"{training_target_dir}/best_params.json") as f:
                    json_dict = json.load(f)
                    best_params = json_dict[config["model_name"]]
            except Exception:
                raise FileNotFoundError(
                    f"Could not find {config['model_name']} in current data. Try to run an hyperoptimization by setting `perform_hyperoptimization` to true"
                )

        # Perform cross-validation of the best model on k-folds of train + val set
        if perform_crossval:
            x_train_val = pd.concat([x_train, x_val], axis=0)
            y_train_val = pd.concat([y_train, y_val], axis=0)
            n_splits = 4
            n_samples = len(x_train_val)
            test_size = int(n_samples / (n_splits + 4))
            tscv = TimeSeriesSplit(n_splits=n_splits, test_size=test_size)

            # Store the scores
            cross_validation_scores = []

            for i, (train_index, val_index) in enumerate(tscv.split(x_train_val)):
                _type_name = f"crossval_fold_{i}"

                if DATE_COLUMN:
                    date_column = train[DATE_COLUMN].copy()

                    if config.get("need_scaling"):
                        date_column = date_column.map(pd.Timestamp.fromordinal)

                    # Now you can use the actual train/val indices to extract ranges
                    train_start = date_column.iloc[train_index[0]]
                    train_end = date_column.iloc[train_index[-1]]
                    val_start = date_column.iloc[val_index[0]]
                    val_end = date_column.iloc[val_index[-1]]

                    logger.info(
                        f"[Fold {i}] Train: {len(train_index)} samples from {train_start.date()} to {train_end.date()} | "
                        f"Validation: {len(val_index)} samples from {val_start.date()} to {val_end.date()}"
                    )
                else:
                    logger.info(
                        f"[Fold {i}] Train: {len(train_index)} samples | Validation: {len(val_index)} samples"
                    )

                # Train the model and get the score
                if config["recurrent"]:
                    cross_validation_score, _, _ = train_model(
                        params=best_params,
                        x_train=x_train_val[train_index],
                        y_train=y_train_val[train_index],
                        x_val=x_train_val[val_index],
                        y_val=y_train_val[val_index],
                        config=config,
                    )
                else:
                    cross_validation_score, _, _ = train_model(
                        params=best_params,
                        x_train=x_train_val.iloc[train_index],
                        y_train=y_train_val.iloc[train_index],
                        x_val=x_train_val.iloc[val_index],
                        y_val=y_train_val.iloc[val_index],
                        config=config,
                    )

                # Append score to the list
                cross_validation_scores.append(cross_validation_score)

            # Calculate and log the mean score
            cross_validation_mean_score = pd.DataFrame(cross_validation_scores)[
                metric
            ].mean()
            logger.info(
                f"Best model mean cross-validation score: {cross_validation_mean_score}"
            )

            # Retrain on entire training set, but keep score on cross-validation folds
            best_score, best_model, best_pred = train_model(
                params=best_params,
                x_train=x_train,
                y_train=y_train,
                x_val=x_val,
                y_val=y_val,
                config=config,
            )
            best_score = cross_validation_mean_score
        else:
            # Evaluate on validation set
            _type_name = "validation"
            best_score, best_model, best_pred = train_model(
                params=best_params,
                x_train=x_train,
                y_train=y_train,
                x_val=x_val,
                y_val=y_val,
                config=config,
            )

            logger.info(f"Best model scores on validation set: {best_score}")

        # Save validation predictions
        best_pred.to_csv(
            f"{results_dir}/pred_val.csv",
            index=True,
            header=True,
            index_label="ID",
        )

        # Save best model
        if config["recurrent"]:
            model_path = f"{results_dir}/{best_model.model_name}.keras"
            best_model.save(model_path)
        else:
            model_path = f"{results_dir}/{best_model.model_name}.best"
            joblib.dump(best_model, model_path)

        model_path = Path(model_path).resolve()
        best_score["MODEL_PATH"] = model_path

        # Track scores
        scores_tracking_path = f"{training_target_dir}/scores_tracking.csv"
        best_score_df = pd.DataFrame([best_score])

        if os.path.exists(scores_tracking_path):
            existing_scores = pd.read_csv(scores_tracking_path)
            common_cols = existing_scores.columns.intersection(best_score_df.columns)
            best_score_df = best_score_df[common_cols]
            scores_tracking = pd.concat(
                [existing_scores, best_score_df], ignore_index=True
            )
        else:
            scores_tracking = best_score_df

        scores_tracking.sort_values(metric, ascending=True, inplace=True)
        scores_tracking.to_csv(scores_tracking_path, index=False)

        # Save model training metadata
        stop = time.time()
        training_time = stop - start
        model_training.best_params = best_params
        model_training.model_path = model_path
        model_training.training_time = training_time
        model_training.save()

        # Store metrics in DB
        drop_cols = [
            "DATE",
            "SESSION",
            "TRAIN_DATA",
            "VAL_DATA",
            "FEATURES",
            "MODEL_NAME",
            "MODEL_PATH",
        ]
        best_score = {k: v for k, v in best_score.items() if k not in drop_cols}
        score_data = {k.lower(): v for k, v in best_score.items()}

        Score.upsert(
            match_fields=["model_training_id"],
            model_training_id=model_training.id,
            **score_data,
        )

        logger.info(f"Model training finished in {training_time:.2f} seconds")

    # find best model type
    scores_tracking_path = f"{training_target_dir}/scores_tracking.csv"
    scores_tracking = pd.read_csv(scores_tracking_path)
    best_score_overall = scores_tracking.iloc[0, :]
    best_model_name = best_score_overall["MODEL_NAME"]

    # Remove any .best or .keras files
    for file_path in glob.glob(os.path.join(training_target_dir, "*.best")) + glob.glob(
        os.path.join(training_target_dir, "*.keras")
    ):
        os.remove(file_path)
    # Copy the best model in root training folder for this target
    best_model_path = Path(
        f"{training_target_dir}/{os.path.basename(best_score_overall['MODEL_PATH'])}"
    ).resolve()
    copy_any(
        best_score_overall["MODEL_PATH"],
        best_model_path,
    )

    with open(f"{training_target_dir}/best_params.json", "r") as f:
        best_model_params = json.load(f)[best_model_name]

    # save model_selection results to db
    model_selection = ModelSelection.get(model_selection.id)
    model_selection.best_model_id = Model.find_by(
        name=best_score_overall["MODEL_NAME"], type=_target_type
    ).id
    model_selection.best_model_params = best_model_params
    model_selection.best_model_path = best_model_path
    model_selection.save()

    logger.info(f"Best model overall is : {best_score_overall}")


def collect_error_logs(training_target_dir: int, storage_path: str):

    output_error_file = f"{training_target_dir}/errors.log"

    with open(output_error_file, "a") as outfile:
        # Walk through the ray_results directory
        for root, dirs, files in os.walk(storage_path):
            # Check if 'error.txt' exists in the current directory
            if "error.txt" in files:
                error_file_path = os.path.join(root, "error.txt")
                logger.info(f"Processing error file: {error_file_path}")
                # Read and append the content of the error.txt file
                with open(error_file_path, "r") as infile:
                    outfile.write(f"\n\n=== Error from {error_file_path} ===\n")
                    outfile.write(infile.read())
    logger.info(f"All errors written to {output_error_file}")


def plot_evaluation_for_classification(prediction: dict):
    """
    Args
        prediction (pd.DataFrame): Should be a df with TARGET, PRED, 0, 1 columns for y_true value (TARGET), y_pred (PRED), and probabilities (for classification only : 0 and 1)
    """
    y_true = prediction["TARGET"]
    y_pred = prediction["PRED"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    # Plot confusion matrix
    plot_confusion_matrix(y_true, y_pred)

    # Compute ROC curve and ROC area
    fpr, tpr, thresholds = roc_curve(y_true, y_pred_proba)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 8))
    plt.plot(
        fpr, tpr, color="darkorange", lw=2, label="ROC curve (area = %0.2f)" % roc_auc
    )
    plt.plot([0, 1], [0, 1], color="navy", lw=2, linestyle="--")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.show()

    # Compute precision-recall curve
    precision, recall, _ = precision_recall_curve(y_true, y_pred_proba)
    average_precision = average_precision_score(y_true, y_pred_proba)

    plt.figure(figsize=(8, 8))
    plt.step(recall, precision, color="b", alpha=0.2, where="post")
    plt.fill_between(recall, precision, step="post", alpha=0.2, color="b")
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])
    plt.title("Precision-Recall Curve: AP={0:0.2f}".format(average_precision))
    plt.show()


def plot_confusion_matrix(y_true, y_pred):
    unique_labels = np.unique(np.concatenate((y_true, y_pred)))
    cm = confusion_matrix(y_true, y_pred)

    labels = np.sort(unique_labels)  # Sort labels based on numerical order

    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt="d", cmap="viridis")
    plt.xlabel("Predicted", fontsize=12)
    plt.ylabel("True", fontsize=12)
    plt.title("Confusion Matrix", fontsize=14)

    plt.xticks(ticks=np.arange(len(labels)), labels=labels, fontsize=10)
    plt.yticks(ticks=np.arange(len(labels)), labels=labels, fontsize=10)

    plt.show()


# THRESHOLD
def find_max_f1_threshold(prediction):
    """
    Finds the threshold that maximizes the F1 score for a binary classification task.

    Parameters:
    - prediction: DataFrame with 'TARGET' and '1' (predicted probabilities) columns

    Returns:
    - best_threshold: The threshold that maximizes the F1 score
    - best_precision: The precision at that threshold
    - best_recall: The recall at that threshold
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    # Compute precision, recall, and thresholds
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # Drop the first element to align with thresholds
    precision = precision[1:]
    recall = recall[1:]

    # Filter out trivial cases (precision or recall = 0)
    valid = (precision > 0) & (recall > 0)
    if not np.any(valid):
        raise ValueError("No valid threshold with non-zero precision and recall")

    precision = precision[valid]
    recall = recall[valid]
    thresholds = thresholds[valid]

    # Compute F1 scores for each threshold
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)

    best_index = np.argmax(f1_scores)

    best_threshold = thresholds[best_index]
    best_precision = precision[best_index]
    best_recall = recall[best_index]

    return best_threshold, best_precision, best_recall


def find_best_f1_threshold(prediction, fscore_target: float):
    """
    Finds the highest threshold achieving at least the given F1 score target.

    Parameters:
    - prediction: DataFrame with 'TARGET' and '1' (or 1 as int) columns
    - fscore_target: Desired minimum F1 score (between 0 and 1)

    Returns:
    - best_threshold: The highest threshold meeting the F1 target
    - best_precision: Precision at that threshold
    - best_recall: Recall at that threshold
    - best_f1: Actual F1 score at that threshold
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # Align precision/recall with thresholds
    precision = precision[1:]
    recall = recall[1:]
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)

    # Filter for thresholds meeting F1 target
    valid_indices = [i for i, f1 in enumerate(f1_scores) if f1 >= fscore_target]

    if not valid_indices:
        raise ValueError(f"Could not find a threshold with F1 >= {fscore_target:.2f}")

    # Pick the highest threshold among valid ones
    best_index = valid_indices[-1]

    return (
        thresholds[best_index],
        precision[best_index],
        recall[best_index],
        f1_scores[best_index],
    )


def find_max_precision_threshold_without_trivial_case(prediction: dict):
    """
    Finds the threshold that maximizes precision without reaching a precision of 1,
    which indicates all predictions are classified as the negative class (0).

    Parameters:
    - prediction: dict with keys 'TARGET' (true labels) and '1' (predicted probabilities)

    Returns:
    - threshold: the probability threshold that maximizes precision
    - actual_recall: the recall achieved at this threshold
    - actual_precision: the precision achieved at this threshold
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    # Compute precision, recall, and thresholds
    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # Drop the first element of precision and recall to align with thresholds
    precision = precision[1:]
    recall = recall[1:]

    # Filter out precision == 1.0 (which might correspond to predicting only 0s)
    valid_indices = np.where(precision < 1.0)[0]
    if len(valid_indices) == 0:
        raise ValueError("No valid precision values less than 1.0")

    precision = precision[valid_indices]
    recall = recall[valid_indices]
    thresholds = thresholds[valid_indices]

    # Find the index of the maximum precision
    best_index = np.argmax(precision)

    # Return the corresponding threshold, precision, and recall
    best_threshold = thresholds[best_index]
    best_precision = precision[best_index]
    best_recall = recall[best_index]

    return best_threshold, best_precision, best_recall


def find_best_precision_threshold(prediction, precision_target: float = 0.80):
    """
    Finds the highest threshold that achieves at least the given precision target.

    Parameters:
        prediction (pd.DataFrame): DataFrame with columns 'TARGET' and '1' or index 1 for predicted probabilities
        precision_target (float): Desired minimum precision (between 0 and 1)

    Returns:
        tuple: (threshold, precision, recall) achieving the desired precision
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # Align lengths: thresholds is N-1 compared to precision/recall
    thresholds = thresholds
    precision = precision[1:]  # Shift to match thresholds
    recall = recall[1:]

    valid_indices = [i for i, p in enumerate(precision) if p >= precision_target]

    if not valid_indices:
        raise ValueError(
            f"Could not find a threshold with precision >= {precision_target}"
        )

    best_idx = valid_indices[-1]  # Highest threshold with precision >= target

    return thresholds[best_idx], precision[best_idx], recall[best_idx]


def find_best_recall_threshold(prediction, recall_target: float = 0.98) -> float:
    """
    Finds the highest threshold that achieves at least the given recall target.

    Parameters:
        pred_df (pd.DataFrame): DataFrame with columns 'y_true' and 'y_pred_proba'
        recall_target (float): Desired minimum recall (between 0 and 1)

    Returns:
        float: Best threshold achieving the desired recall, or None if not reachable
    """
    y_true = prediction["TARGET"]
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]

    precision, recall, thresholds = precision_recall_curve(y_true, y_pred_proba)

    # `thresholds` has length N-1 compared to precision and recall
    recall = recall[1:]  # Drop first element to align with thresholds
    precision = precision[1:]

    valid_indices = [i for i, r in enumerate(recall) if r >= recall_target]

    if not valid_indices:
        logger.warning(f"Could not find a threshold with recall >= {recall_target}")
        return None, None, None

    best_idx = valid_indices[-1]  # Highest threshold with recall >= target

    return thresholds[best_idx], precision[best_idx], recall[best_idx]


def plot_threshold(prediction, threshold, precision, recall):
    y_pred_proba = prediction[1] if 1 in prediction.columns else prediction["1"]
    y_true = prediction["TARGET"]

    predicted_positive = (y_pred_proba >= threshold).sum()
    predicted_negative = (y_pred_proba < threshold).sum()
    f1_scores = 2 * (precision * recall) / (precision + recall + 1e-10)
    per_predicted_positive = predicted_positive / len(y_pred_proba)
    per_predicted_negative = predicted_negative / len(y_pred_proba)

    logger.info(
        f"""Threshold: {threshold*100:.2f}
        Precision: {precision*100:.2f}
        Recall: {recall*100:.2f}
        F1-score: {f1_scores*100:.2f}
        % of score over {threshold}: {predicted_positive}/{len(y_pred_proba)} = {per_predicted_positive*100:.2f}%
        % of score under {threshold}: {predicted_negative}/{len(y_pred_proba)} = {per_predicted_negative*100:.2f}%"""
    )

    # Visualizing the scores of positive and negative classes
    plt.figure(figsize=(10, 6))
    sns.histplot(
        y_pred_proba[y_true == 1],
        color="blue",
        label="Positive Class",
        bins=30,
        kde=True,
        alpha=0.6,
    )
    sns.histplot(
        y_pred_proba[y_true == 0],
        color="red",
        label="Negative Class",
        bins=30,
        kde=True,
        alpha=0.6,
    )
    plt.axvline(
        x=threshold,
        color="green",
        linestyle="--",
        label=f"Threshold at {round(threshold,3)}",
    )
    plt.title("Distribution of Predicted Probabilities")
    plt.xlabel("Predicted Probabilities")
    plt.ylabel("Frequency")
    plt.legend()
    plt.show()
    return threshold


def print_scores(training_target_dir: str):
    """
    Monitor scores
    """
    scores_tracking = pd.read_csv(f"{training_target_dir}/scores_tracking.csv")
    return scores_tracking


# OLD - to sort out
def get_pred_distribution(training_target_dir: str, model_name="linear"):
    """
    Look at prediction distributions
    """
    prediction = pd.read_csv(
        f"{training_target_dir}/{model_name}/pred_val.csv",
        index_col="ID",
    )
    prediction.describe()


def plot_feature_importance(training_target_dir: str, model_name="linear"):
    """
    Monitor feature importance ranking to filter out unrelevant features
    """
    model = joblib.load(f"{training_target_dir}/{model_name}/{model_name}.best")
    if hasattr(model, "feature_importances_"):
        feature_importances_ = model.feature_importances_.flatten()
    elif hasattr(model, "feature_importance"):
        feature_importances_ = model.feature_importance.flatten()
    elif hasattr(model, "coefs_"):
        feature_importances_ = np.mean(model.coefs_[0], axis=1).flatten()
    elif hasattr(model, "coef_"):
        feature_importances_ = model.coef_.flatten()
    else:
        feature_importances_ = []

    sns.barplot(
        data=feature_importances_,
        orient="h",
    )


def print_model_estimators(training_target_dir: str, model_name="linear"):
    """
    Look at a specific trained model
    """
    model = joblib.load(f"{training_target_dir}/{model_name}/{model_name}.best")
    for i in range(0, 100):
        logger.info(model.estimators_[i].get_depth())


def get_model_info(model):
    model.count_params()
    model.summary()
