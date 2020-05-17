import pytest
import Anton.server as server
import Anton.client as client
from Anton.server import *
from Anton.client import *


def test_reader():
    import Anton.snapshot_reader as rdr
    reader = rdr.SampleReader("./tests/mock_data/1_sample.mind.gzip")

    error_msg = f'Failed in reader, {0}'

    assert reader.user_id == 42, error_msg.format("user_id")
    assert reader.username == "Dan Gittik", error_msg.format("username")
    assert reader.gender == 0, error_msg.format("gender")
    assert reader.birth_date == 699746400, error_msg.format("birthday")


def client_server_fixture(publish=print, path=None):
    import multiprocessing
    import time

    _server = multiprocessing.Process(target=server.run_server, kwargs=dict(host='127.0.0.1', port=7777, publish=publish))
    _server.start()
    time.sleep(2)

    if path:
        client.upload_sample(host='127.0.0.1', port=7777, path=path)

    _server.terminate()
    return True


def test_server_sanity():
    assert client_server_fixture(), "Failed in server sanity"


def test_server_client_1sample():
    assert client_server_fixture(path='./tests/mock_data/1_sample.mind.gzip'), "Failed in 1 snapshot client-server test"


def test_server_client_3sample():
    assert client_server_fixture(path='./tests/mock_data/3_sample.mind.gzip'), "Failed in 3 snapshots client-server test"


def test_error_handle_client():
    with pytest.raises(SystemExit) as se:
        client.upload_sample('127.0.0.1', port=7777, path="./tests/mock_data/.")  # Directory
    assert se.value.code == ERRNO_FILE_NOT_EXIST

    with pytest.raises(SystemExit) as se:
        client.upload_sample('127.0.0.1', port=7777, path="./tests/mock_data/WTFWTWFTWFW")  # No such file
    assert se.value.code == ERRNO_FILE_NOT_EXIST

    with pytest.raises(SystemExit) as se:
        client.upload_sample('127.0.0.1', port=7777, path="./tests/mock_data/mock.raw")  # Not .gz file
    assert se.value.code == ERRNO_FILE_NOT_GZIP

    with pytest.raises(SystemExit) as se:
        client.upload_sample('127.0.0.1', port=7777, path="./tests/mock_data/1_sample.mind.gzip")  # No server available
    assert se.value.code == ERRNO_SERVER_UNAVAILABLE


def test_error_handle_server():
    with pytest.raises(SystemExit) as se:
        server.run_server('127.0.0.1', port=1, publish=print)  # Can't bind host:port
    assert se.value.code == ERRNO_FILE_NOT_EXIST

    with pytest.raises(SystemExit) as se:
        server.run_server('127.0.0.1', port=7777, publish="mongodb://127.0.0.1:27017")  # Unsupported publisher
    assert se.value.code == ERRNO_UNSUPPORTED_SCHEME
