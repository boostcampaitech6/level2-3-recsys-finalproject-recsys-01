# 프로젝트 소개
“나만의 장바구니” 는 사용자의 요리 이력을 기반으로 다음에 요리할 레시피와 해당 레시피를 만드는 데 필요한 재료 목록을 추천하는 서비스 입니다.

## preview

# 진행 기간
2024.02.28 ~ 2024.03.27

# 멤버
<table align="center">
  <tr height="205px">
    <td align="center" width="200px">
      <a href="https://github.com/sangwoonoel"><img src="https://github.com/sangwoonoel.png" width="150px;" alt=""/></a>
    </td>
    <td align="center" width="200px">
      <a href="https://github.com/twndus"><img src="https://github.com/twndus.png" width="150px;" alt=""/></a>
    </td>
    <td align="center" width="200px">
      <a href="https://github.com/uhhyunjoo"><img src="https://github.com/uhhyunjoo.png" width="150px;" alt=""/></a>
    </td>
    <td align="center" width="200px">
      <a href="https://github.com/GangBean"><img src="https://github.com/GangBean.png" width="150px;" alt=""/></a>
    </td>
  </tr>
  <tr>
    <td align="center" width="200px">
      <a href="https://github.com/sangwoonoel">신상우</a>
    </td>
    <td align="center" width="200px">
      <a href="https://github.com/twndus">이주연</a>
    </td>
    <td align="center" width="200px">
      <a href="https://github.com/uhhyunjoo">이현주</a>
    </td>
    <td align="center" width="200px">
      <a href="https://github.com/GangBean">조성홍</a>
    </td>
  </tr>
  <tr>
    <td width="200px">
      <br>
      • 레시피 서비스 기능 API 구현 <br>
      • 데이터 정제 <br>
      • ML modeling <br>
      • MLflow를 이용한 ML 라이플 사이클 관리 <br>
    </td>
    <td width="200px">
      <br>
      • 프론트엔드 구현 <br>
      • 최적화 알고리즘 설계 <br>
      • 데이터 크롤링 <br>
      • ML modeling & serving <br>
    </td>
    <td width="200px">
      <br>
      • 프론트엔드 구현 <br>
      • 데이터 크롤링 및 전처리 <br>
      • DB 업데이트 자동화 <br>
    </td>
    <td width="200px">
      <br> 
      • 유저 서비스 기능 API 구현 <br>
      • 장바구니 추천 API 구현 <br>
      • 데이터 수집 <br>
      • 데이터베이스 설정 <br>
    </td>
  </tr>
</table>
&nbsp;

# 사용 기술

# 서비스 아키텍처
1. App 서버 : Front / Back 을 구분하여 운영 ([Streamlit](https://streamlit.io/) / [FastAPI](https://fastapi.tiangolo.com/ko/))
2. DB 서버 : 레시피 및 인터렉션 데이터 저장, 가격 데이터 저장 (MongoDB)
3. Crawl 서버 : 크롤링 및 데이터 정제 수행 ([Airflow](https://airflow.apache.org/), [Selenium](https://www.selenium.dev/))
4. ML 서버 : 배치 서빙 및 학습 자동화, 모델 관리 ([Airflow](https://airflow.apache.org/), [MLflow](https://mlflow.org/))

1. **크롤링 자동화**
    - Airflow를 이용해 매일 새로운 학습 데이터(레시피 및 인터렉션 데이터) 수집, 이후 프롬프트 엔지니어링을 통해 레시피의 식재료명 정제 작업 진행
    - 식제료명 정제 작업 이후, 정제된 식재료 명을 기반으로 매일 식재료 가격 정보를 새롭게 수집
2. **배치 서빙 및 학습 자동화**
    - Airflow를 이용해 매일 배치 서빙 진행, 매주 모델 재학습
    - MLflow를 이용해 모델 학습을 트래킹하고 모델 버전 관리
  
# 참고 자료
https://youtu.be/kUTHhSbEgLs
