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


@pytest.mark.parametrize("host, port, database_name", [
    ('localhost', '27017', 'dev'),
    ('10.0.6.6', '27017', 'prod'),
])
def test_데이터베이스_반환_정상(host, port, database_name):
    # given
    config = {
        'host': host,
        'port': port,
        'database_name': database_name
    }
    datasource = DataSource(**config)

    # when
    database = datasource.database()

    # then
    assert database is not None


@pytest.mark.parametrize("host, port, database, collection_name" , [
    ('localhost', '27017', 'dev', 'users'),
    ('localhost', '27017', 'dev', 'recipes'),
    ('localhost', '27017', 'dev', 'ingredients'),
    ('10.0.6.6', '27017', 'prod', 'users'),
    ('10.0.6.6', '27017', 'prod', 'recipes'),
    ('10.0.6.6', '27017', 'prod', 'ingredients'),
])
def test_컬렉션_반환_정상(host, port, database, collection_name):
    # given
    config = {
        'host': host,
        'port': port,
        'database_name': database
    }
    datasource = DataSource(**config)

    # when
    collection = datasource.collection_with_name_as(collection_name)

    # then
    assert collection is not None
