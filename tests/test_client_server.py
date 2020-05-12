import pytest
import Anthon.server as server
import Anthon.client as client


def test_reader():
    import Anthon.snapshot_reader as rdr
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


