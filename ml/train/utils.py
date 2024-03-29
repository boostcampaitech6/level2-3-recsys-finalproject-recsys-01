import os
from pathlib import Path
from recbole.model.general_recommender import BPR
from recbole.model.sequential_recommender import SASRec


def find_latest_file(directory_path):
    # 디렉토리에서 .pth 파일들만 필터링
    pth_files = list(Path(directory_path).glob('*.pth'))
    
    # 파일이 없으면 None 반환
    if not pth_files:
        return None
    # 가장 최근에 수정된 파일 찾기
    latest_pth_file = max(pth_files, key=os.path.getmtime)
    
    return os.path.join(directory_path, latest_pth_file.name)


def get_model(model_name, config, train_data):
    if model_name == "BPR":
        return BPR(config, train_data.dataset).to(config['device'])
    if model_name == "SASRec":
        return SASRec(config, train_data.dataset).to(config['device'])
    

def get_directory_path():
    directory_path = os.getenv('MODEL_SAVE_DIR')
    if directory_path is None:
        raise EnvironmentError("환경변수 'MODEL_SAVE_DIR'가 설정되어 있지 않습니다.")
    return directory_path