import mlflow

from datetime import datetime
from model import get_data_and_model
from utils import find_latest_file, get_directory_path


def train():
    model, trainer, train_data, valid_data, test_data = get_data_and_model()
    with mlflow.start_run():
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        run_name = f"{model.__class__.__name__}_{current_time}"
        mlflow.set_tag("mlflow.runName", run_name)
        
        # 모델 학습
        best_valid_score, best_valid_result = trainer.fit(train_data, valid_data, saved=True, show_progress=True)

        # 테스트 데이터에 대한 평가
        test_result = trainer.evaluate(test_data, load_best_model=True, show_progress=True)

        # MLflow에 파라미터, 메트릭, 모델 로깅
        mlflow.log_metric("best_validation_score", best_valid_score)
        mlflow.pytorch.log_model(model, "model")

        directory_path = get_directory_path()
        # RecBole run의 결과로 생긴 .pth 파일 찾기
        artifact = find_latest_file(directory_path)
        # RecBole .pth 파일 저장 
        mlflow.log_artifact(artifact, artifact_path="recbole")
        
        
if __name__ == "__main__":
    train()