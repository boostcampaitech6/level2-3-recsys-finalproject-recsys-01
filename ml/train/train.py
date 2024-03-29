import mlflow
import os
import yaml

from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.trainer import Trainer
from mlflow.tracking import MlflowClient
from datetime import datetime
from utils import get_model, find_latest_file


# YAML 파일 열기
with open('train.yaml', 'r') as file:
    config = yaml.safe_load(file)

# RecBole 설정 불러오기
config_file_list = config['config_file_list']
config = Config(model=config['model'], dataset=config['dataset'], config_file_list=config_file_list)

# 데이터셋 및 데이터 로더 준비
dataset = create_dataset(config)
train_data, valid_data, test_data = data_preparation(config, dataset)

# 모델 불러오기
model = get_model(config['model'], config, train_data)
trainer = Trainer(config, model)

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

    directory_path = os.getenv('MODEL_SAVE_DIR')
    if directory_path is None:
        raise EnvironmentError("환경변수 'MODEL_SAVE_DIR'가 설정되어 있지 않습니다.")
    
    # RecBole run의 결과로 생긴 .pth 파일 찾기
    artifact = find_latest_file(directory_path)
    # RecBole .pth 파일 저장 
    mlflow.log_artifact(artifact, artifact_path="recbole")