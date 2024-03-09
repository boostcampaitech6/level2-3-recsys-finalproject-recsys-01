import pytest

from ...app.database.data_source import DataSource, env_file_of

@pytest.mark.parametrize("input, output", [
    ('dev', 'dev.env'),
    ('prod', 'prod.env'),
])
def test_환경변수파일_경로찾기_정상(input, output):
    # given
    env = input

    # when
    filename = env_file_of(env).split('/')[-1]

    # then
    assert filename == output

@pytest.mark.parametrize("host, port, database", [
    ('localhost', '27017', 'dev'),
    ('10.0.6.6', '27017', 'prod'),
])
def test_데이터소스_생성_정상(host, port, database):
    # given
    config = {
        'host': host,
        'port': port,
        'database': database
    }

    # when, then
    with pytest.raises(Exception):
        DataSource(**config)