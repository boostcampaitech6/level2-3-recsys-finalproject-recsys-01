import yaml

from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.trainer import Trainer
from utils import get_model


def get_data_and_model():
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
    data_and_model = (model, trainer, train_data, valid_data, test_data)
    return data_and_model