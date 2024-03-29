import mlflow
import os
import yaml

import mlflow.pyfunc
from recbole.quick_start import load_data_and_model
from mlflow.tracking import MlflowClient

    
def serve_model():
    # YAML 파일 열기
    with open('serving.yaml', 'r') as file:
        config = yaml.safe_load(file)
        
    # mlflow로 부터 받아올 모델 저장 경로를 설정
    dst_path = os.getenv("MLFLOW_DST_PATH")
    
    client = MlflowClient()
    # 가져오고 싶은 모델 이름과 버전을 명시
    model_version_details = client.get_model_version(config['model'], config['version'])
    # 모델과 연관된 실행(run) ID 가져오기
    run_id = model_version_details.run_id
    artifacts = client.list_artifacts(run_id, path=config['path'])
    
    artifact = mlflow.artifacts.download_artifacts(
    run_id=run_id,
    artifact_path=artifacts[0].path,
    dst_path=dst_path
    )   
    
    config, model, dataset, train_data, valid_data, test_data = load_data_and_model(
        model_file=artifact,
    )
    
    data_and_model = (config, model, dataset, train_data, valid_data, test_data)
    
    return data_and_model


if __name__ == "__main__":
    serve_model()