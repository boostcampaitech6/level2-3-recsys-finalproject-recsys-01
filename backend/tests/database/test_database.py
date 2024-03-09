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
