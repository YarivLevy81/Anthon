import pytest
import mongomock
from Anthon.saver.__main__ import save
from Anthon.saver.MongoHandler import MongoHandler


@mongomock.patch(servers=(('127.0.0.1', 27017),))
def test_mongo():
    path = "mongodb://127.0.0.1:27017"
    save(database=path, topic='pose', path="./tests/mock_data/pose.result")

    handler = MongoHandler(path=path)
    assert len(handler.get_all_users()) == 1
    assert handler.get_all_users()[0]['user_id'] == 42
    assert handler.get_all_users()[0]['username'] == 'Dan Gittik'
    assert handler.get_user(42)['birthdate'] == 699746400
    assert handler.get_user(42)['gender'] == 0

    assert len(handler.get_user_snapshots(42)) == 1
    assert handler.get_user_snapshots(42)[0]['snapshot_id'] == 'mock'
    assert handler.get_user_snapshots(42)[0]['timestamp'] == 1575446887339

    assert 'pose' in handler.get_snapshot(42, "mock")
    result = handler.get_snapshot(42, "mock")['pose']
    assert result['translation_x'] == 0.4873843491077423
    assert result['translation_y'] == 0.007090016733855009
    assert result['translation_z'] == -1.1306129693984985
    assert result['rotation_x'] == -0.10888676356214629
    assert result['rotation_y'] == -0.26755994585035286
    assert result['rotation_z'] == -0.021271118915446748
    assert result['rotation_w'] == 0.9571326384559261
