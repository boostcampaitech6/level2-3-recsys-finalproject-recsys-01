import mlflow
from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.model.general_recommender import BPR
from recbole.trainer import Trainer
from mlflow.tracking import MlflowClient
from datetime import datetime

# RecBole 설정 불러오기
config_file_list = ['general.yaml']
config = Config(model='BPR', dataset='BasketRecommendation', config_file_list=config_file_list)

# 데이터셋 및 데이터 로더 준비
dataset = create_dataset(config)
train_data, valid_data, test_data = data_preparation(config, dataset)

# 모델 초기화
model = BPR(config, train_data.dataset).to(config['device'])

# trainer 초기화
trainer = Trainer(config, model)

# 명시적으로 지정 가능
"""
mlflow.set_tracking_uri("http://x.x.x.x:xxxx")
exp_info = MlflowClient().get_experiment_by_name("experiment_name")
exp_id = exp_info.experiment_id if exp_info else MlflowClient().create_experiment("experiment_name")
with mlflow.start_run(experiment_id=exp_id) as run:
"""

current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
custom_run_name = f"{model.__class__.__name__}_{current_time}"

with mlflow.start_run(run_name=custom_run_name):
    # 모델 학습
    best_valid_score, best_valid_result = trainer.fit(train_data, valid_data, saved=True, show_progress=True)
    
    # 테스트 데이터에 대한 평가
    test_result = trainer.evaluate(test_data, load_best_model=True, show_progress=True)
    
    # MLflow에 파라미터, 메트릭, 모델 로깅
    mlflow.log_metric("best_validation_score", best_valid_score)
    mlflow.pytorch.log_model(model, 'model')