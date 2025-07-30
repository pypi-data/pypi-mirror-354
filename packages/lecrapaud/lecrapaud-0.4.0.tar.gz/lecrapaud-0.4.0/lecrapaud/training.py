import logging
import joblib
from pathlib import Path
import os
from src.utils import logger

from src.feature_engineering import feature_engineering
from src.feature_selection import (
    create_sets_from_data,
    feature_selection,
    scale_data,
    reshape_time_series,
)
from src.model_selection import model_selection, test_hardware
from src.data_sourcing import get_filtered_data
from src.constants import stock_list_3, stock_list_1
from src.search_space import ml_models, dl_recurrent_models
from src.directory_management import tmp_dir
from src.db.models import Dataset
from src.config import PYTHON_ENV


def run_training(
    dataset_id=None,
    years_of_data=2,
    list_of_groups=stock_list_1,
    percentile=15,
    corr_threshold=80,
    max_features=20,
    max_timesteps=120,
    targets_numbers=range(1, 15),
    models_idx=range(len(ml_models)),
    number_of_trials=20,
    perform_hyperoptimization=True,
    perform_crossval=False,
    clean_dir=False,
    preserve_model=False,
    session_name="test",
):
    logging.captureWarnings(True)

    if dataset_id is None:
        # Get the data
        logger.info("Getting data...")
        data = get_filtered_data(
            years_of_data=years_of_data,
            list_of_groups=list_of_groups,
        )

        # preprocess & feature engineering
        logger.info("Preprocessing...")
        data_for_training = feature_engineering(
            data, for_training=True, save_as_csv=True
        )

        # train / val / test sets
        train, val, test, dataset = create_sets_from_data(
            data_for_training,
            percentile=percentile,
            corr_threshold=corr_threshold,
            max_features=max_features,
        )
        dataset_dir = dataset.path
        dataset_id = dataset.id
        train_data_dir = f"{dataset_dir}/data"
        os.makedirs(train_data_dir, exist_ok=True)
        preprocessing_dir = f"{dataset_dir}/preprocessing"

        # feature selection
        logger.info("Feature Selection...")
        for target_number in targets_numbers:
            feature_selection(
                dataset_id=dataset_id,
                train=train,
                target_number=target_number,
                single_process=True,
            )

        dataset = Dataset.get(dataset_id)
        all_features = dataset.get_all_features()
        columns_to_keep = all_features + [f"TARGET_{i}" for i in range(1, 15)]
        logger.info(columns_to_keep)
        duplicates = [
            col for col in set(columns_to_keep) if columns_to_keep.count(col) > 1
        ]

        if duplicates:
            raise ValueError(f"Doublons détectés dans columns_to_keep: {duplicates}")

        train = train[columns_to_keep]
        val = val[columns_to_keep]
        test = test[columns_to_keep]

        if PYTHON_ENV != "Test":
            joblib.dump(train[columns_to_keep], f"{train_data_dir}/train.pkl")
            joblib.dump(val[columns_to_keep], f"{train_data_dir}/val.pkl")
            joblib.dump(test[columns_to_keep], f"{train_data_dir}/test.pkl")

        # scaling features
        logger.info("Scaling features...")
        train_scaled, scaler_x, scalers_y = scale_data(
            train, save_dir=preprocessing_dir
        )
        val_scaled, _, _ = scale_data(
            val, save_dir=preprocessing_dir, scaler_x=scaler_x, scalers_y=scalers_y
        )
        test_scaled, _, _ = scale_data(
            test, save_dir=preprocessing_dir, scaler_x=scaler_x, scalers_y=scalers_y
        )

        if PYTHON_ENV != "Test":
            joblib.dump(train_scaled, f"{train_data_dir}/train_scaled.pkl")
            joblib.dump(val_scaled, f"{train_data_dir}/val_scaled.pkl")
            joblib.dump(test_scaled, f"{train_data_dir}/test_scaled.pkl")

        data = {
            "train": train,
            "val": val,
            "test": test,
            "train_scaled": train_scaled,
            "val_scaled": val_scaled,
            "test_scaled": test_scaled,
            "scalers_y": scalers_y,
        }

    list_models = ml_models + dl_recurrent_models
    reshaped_data = None
    if any(list_models[i].get("recurrent") for i in models_idx):
        # reshaping data for recurrent models
        logger.info("Reshaping data for recurrent models...")
        reshaped_data = reshape_time_series(
            train_scaled, val_scaled, test_scaled, all_features, timesteps=max_timesteps
        )

    # model selection and hyperoptimization
    logger.info("Model Selection and Hyperoptimization...")
    for target_number in targets_numbers:
        model_selection(
            dataset_id=dataset_id,
            models_idx=models_idx,
            target_number=target_number,
            session_name=session_name,
            perform_hyperoptimization=perform_hyperoptimization,
            perform_crossval=perform_crossval,
            number_of_trials=number_of_trials,
            plot=False,
            clean_dir=clean_dir,
            preserve_model=preserve_model,
            reshaped_data=reshaped_data,
            data=(data or None),
        )
