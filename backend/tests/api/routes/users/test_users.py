import pytest

def test_회원가입_필수입력누락_오류():
    # given
    # POST /api/users
    # 입력: login_id, login_password, nickname, email
    # 출력: 400 Bad Request: 필수 입력값이 누락되거나 입력값의 형태가 틀림
    pass

def test_회원가입_필수입력검증_오류():
    # given
    # POST /api/users
    # 입력: login_id, login_password, nickname, email
    # 출력: 400 Bad Request: 필수 입력값이 누락되거나 입력값의 형태가 틀림
    pass

def test_회원가입_아이디중복_오류():
    # GET /api/users?login_id={login_id}
    # - 400 Bad Request:
    # 409 Conflict: 이미 존재하는 아이디인 경우
    pass

def test_회원가입_닉네임중복_오류():
    # GET /api/users?nickname={nickname}
    # 409 Conflict: 이미 존재하는 닉네임인 경우
    pass

def test_회원가입_정상():
    # POST /api/users
    # 입력: login_id, login_password, nickname, email
    # 출력: 400 Bad Request: 필수 입력값이 누락되거나 입력값의 형태가 틀림

    pass

def test_로그인_필수입력누락_오류():
    # POST /api/users/auths
    # - 입력: login_id, login_password
    # 출력: session id, 201 Created
    pass

def test_로그인_필수입력검증_오류():
    # POST /api/users/auths
    # - 입력: login_id, login_password
    # 출력: session id, 201 Created
    pass

def test_로그인_로그인아이디미존재_오류():
    # POST /api/users/auths
    # - 입력: login_id, login_password
    # 출력: session id, 201 Created
    pass

def test_로그인_비밀번호불일치_오류():
    # POST /api/users/auths
    # - 입력: login_id, login_password
    # 출력: session id, 201 Created
    pass

def test_로그인_정상():
    # POST /api/users/auths
    # - 입력: login_id, login_password
    # 출력: session id, 201 Created
    pass

def test_선호음식_리스트조회_미로그인_오류():
    # GET /api/foods?page={page_num}
    # 출력: List[음식], next_page_url 200 OK(없을 경우 비운채로)
    # 401 Unauthorized: 로그인 안 한 상태
    pass

def test_선호음식_리스트조회_정상():
    # GET /api/foods?page={page_num}
    # 출력: List[음식], next_page_url 200 OK(없을 경우 비운채로)
    # 401 Unauthorized: 로그인 안 한 상태
    pass

def test_선호음식_리스트조회_페이지네이션():
    # GET /api/foods?page={page_num}
    # 출력: List[음식], next_page_url 200 OK(없을 경우 비운채로)
    # 401 Unauthorized: 로그인 안 한 상태
    pass

def test_선호음식저장_개수부족_오류():
    # POST /api/users/{user_id}/foods
    # 입력: user_id, List[food_id]
    # 출력: 201 Created
    # 에러
    # 400 Bad Request: 입력값 누락(필요 최소 재료개수 등)
    # 401 Unauthorized: 로그인 안 한 상태
    # 500 Internal Server Error: 관리자에게 문의하세요.
    pass

def test_선호음식저장_미로그인_오류():
    # POST /api/users/{user_id}/foods
    # 입력: user_id, List[food_id]
    # 출력: 201 Created
    # 에러
    # 400 Bad Request: 입력값 누락(필요 최소 재료개수 등)
    # 401 Unauthorized: 로그인 안 한 상태
    # 500 Internal Server Error: 관리자에게 문의하세요.
    pass

def test_선호음식저장_정상():
    # POST /api/users/{user_id}/foods
    # 입력: user_id, List[food_id]
    # 출력: 201 Created
    # 에러
    # 400 Bad Request: 입력값 누락(필요 최소 재료개수 등)
    # 401 Unauthorized: 로그인 안 한 상태
    # 500 Internal Server Error: 관리자에게 문의하세요.
    pass
