import mlflow
import os
import mlflow.pyfunc
from recbole.quick_start import load_data_and_model
import mlflow.pyfunc


# 환경변수에서 값 읽기
run_id = os.getenv("MLFLOW_RUN_ID", "default_run_id")  # 기본값 설정 가능
artifact_path = os.getenv("MLFLOW_ARTIFACT_PATH", "default_artifact_path")
dst_path = os.getenv("MLFLOW_DST_PATH", "default_dst_path")
model_file_path = mlflow.artifacts.download_artifacts(run_id=run_id, artifact_path=artifact_path, dst_path=dst_path)

config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
    model_file=model_file_path,
)