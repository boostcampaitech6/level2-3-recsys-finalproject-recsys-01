from ...app.database.data_source import DataSource, env_file_of

def test_환경변수파일_경로찾기_정상():
    # given
    env = 'dev'

    # when
    filename = env_file_of(env).split('/')[-1]

    # then
    assert filename == 'dev.env'
