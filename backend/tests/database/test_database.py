import pytest

from ...app.database.data_source import DataSource, env_file_of
from ..assert_not_raises import not_raises

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
        'database_name': database
    }

    # when, then
    with not_raises(Exception):
        DataSource(**config)


@pytest.mark.parametrize("host, port, database", [
    ('localhost', '27017', 'dev'),
    ('10.0.6.6', '27017', 'prod'),
])
def test_데이터베이스_반환_정상(host, port, database):
    # given
    config = {
        'host': host,
        'port': port,
        'database_name': database
    }
    datasource = DataSource(**config)

    # when
    result = datasource.database()

    # then
    assert result is not None
