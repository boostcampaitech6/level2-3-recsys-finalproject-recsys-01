from typing import List

import torch

from recbole.config import Config
from recbole.data import create_dataset, data_preparation
from recbole.model.general_recommender import MultiDAE # BPR
from recbole.trainer import Trainer
from recbole.utils import init_logger, init_seed
from recbole.data.interaction import Interaction

def inference(user_ids: List[str], modelname: str, config_file: str, model_file_path: str, k: int=20):
    
    # 설정 파일 로드
    config = Config(model=modelname, dataset='recipe-dataset', config_file_list=[config_file])

    # 데이터셋 생성
    dataset = create_dataset(config)

    # 데이터 분할
    train_data, valid_data, test_data = data_preparation(config, dataset)

    # 모델 초기화
    if modelname == 'MultiDAE':
        model = MultiDAE(config, train_data.dataset).to(config['device'])
    else:
        raise ValueError(f'{modelname} Not Found. Train First')

    # 모델 파라미터 로드
    model.load_state_dict(torch.load(model_file_path)['state_dict'])

    # 추론 준비
    model.eval()

    # 사용자 ID에 대한 텐서 생성
    user_ids = [dataset.token2id(dataset.uid_field, user_id) for user_id in user_ids]
    user_dict = {
        dataset.uid_field: torch.tensor(user_ids, dtype=torch.int64).to(config['device'])
    }

    # Interaction 객체 생성
    interaction = Interaction(user_dict)

    # 모델을 사용하여 추천 생성
    scores = model.full_sort_predict(interaction).view(-1, dataset.item_num)
    probas = torch.sigmoid(scores)

    # 실제 인터렉션이 있는 위치를 매우 낮은 값으로 마스킹
    user_interactions = model.get_rating_matrix(interaction['user_id'])
    masked_scores = probas.clone()
    masked_scores[user_interactions >= 1] = -1e9

    # 확률이 높은 아이템 20개 추출 
    topk_proba, topk_item = torch.topk(masked_scores, k, dim=1)

    item_ids = [
        dataset.id2token(dataset.iid_field, item_token).tolist()\
            for item_token in topk_item.detach().cpu().numpy()]
    item_proba = topk_proba.detach().cpu().numpy()

    print(item_ids)
    print(item_proba)

    return {'item_ids': item_ids, 'item_proba': item_proba.tolist()}

if __name__ == '__main__':

    # 설정 파일과 모델 저장 경로 설정
    config_file_path = '/home/judy/train_model/recipe-dataset.yaml'  # 설정 파일 경로
    model_file_path = '/home/judy/train_model/saved/MultiDAE-Mar-14-2024_23-15-20.pth'  # 모델 파일 경로

    recommended_items = inference(
        user_ids=['76017883', '94541740'], 
        modelname='MultiDAE', 
        config_file=config_file_path, 
        model_file_path=model_file_path, 
        k=20)

    print(recommended_items['item_ids'])
    print(recommended_items['item_proba'])
