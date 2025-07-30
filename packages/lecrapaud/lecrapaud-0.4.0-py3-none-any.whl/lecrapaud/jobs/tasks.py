from src.jobs import app

# from honeybadger import honeybadger
from src.send_daily_emails import send_daily_emails
from src.config import DATASET_ID, RECEIVER_EMAIL
from src.training import run_training
from src.constants import stock_list_3
from src.search_space import get_models_idx


@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    acks_late=True,
)
def task_send_daily_emails(self):
    try:
        print(f"[Attempt #{self.request.retries}] task_send_daily_emails")
        dataset_id = int(DATASET_ID)
        email = RECEIVER_EMAIL
        return send_daily_emails(email, dataset_id)
    except Exception as e:
        print(e)
        # honeybadger.notify(e)
        raise


@app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 5},
    acks_late=True,
)
def task_training_experiment(self):
    try:
        print(f"[Attempt #{self.request.retries}] task_training_experiment")
        run_training(
            years_of_data=20,
            list_of_groups=stock_list_3,
            targets_numbers=range(1, 15),
            percentile=20,
            corr_threshold=80,
            max_features=25,
            models_idx=get_models_idx("linear", "xgb"),
            number_of_trials=20,
            perform_hyperoptimization=True,
            perform_crossval=False,
            preserve_model=False,
            session_name="20y_stock_list_3_linear_xgb",
        )
    except Exception as e:
        print(e)
        # honeybadger.notify(e)
        raise
