import json
from Anton.parsers import parse


def test_pose_parser():
    result = parse(parser_type='pose', path="./tests/mock_data/mock.raw")
    err_msg = f'Failed in pose parser at {0}'
    result = json.loads(result)

    assert 'pose' in result
    result = result['pose']

    assert result['translation_x'] == 0.4873843491077423, err_msg.format('translation_x')
    assert result['translation_y'] == 0.007090016733855009, err_msg.format('translation_y')
    assert result['translation_z'] == -1.1306129693984985, err_msg.format('translation_z')
    assert result['rotation_x'] == -0.10888676356214629, err_msg.format('rotation_x')
    assert result['rotation_y'] == -0.26755994585035286, err_msg.format('rotation_y')
    assert result['rotation_z'] == -0.021271118915446748, err_msg.format('rotation_z')
    assert result['rotation_w'] == 0.9571326384559261, err_msg.format('rotation_w')


def test_color_image_parser():
    result = parse(parser_type='color_image', path="./tests/mock_data/mock.raw")
    err_msg = f'Failed in color_image parser at {0}'
    result = json.loads(result)

    assert 'color_image' in result
    result = result['color_image']

    assert result['height'] == 1080, err_msg.format('height')
    assert result['width'] == 1920, err_msg.format('width')

    from pathlib import Path
    expected_path = str(Path().cwd().absolute()) + "/users_data/42/mock/color_image.png"
    assert result['image_path'] == expected_path, err_msg.format('image_path')


def test_depth_image_parser():
    result = parse(parser_type='depth_image', path="./tests/mock_data/mock.raw")
    err_msg = f'Failed in depth_image parser at {0}'
    result = json.loads(result)

    assert 'depth_image' in result
    result = result['depth_image']

    assert result['height'] == 1080, err_msg.format('height')
    assert result['width'] == 1920, err_msg.format('width')

    from pathlib import Path
    expected_path = str(Path().cwd().absolute()) + "/users_data/42/mock/depth_image.png"
    assert result['image_path'] == expected_path, err_msg.format('image_path')


def test_feelings_parser():
    result = parse(parser_type='feelings', path="./tests/mock_data/mock.raw")
    err_msg = f'Failed in feelings parser at {0}'
    result = json.loads(result)

    assert 'feelings' in result
    result = result['feelings']

    assert result['hunger'] == 0.0, err_msg.format('hunger')
    assert result['thirst'] == 0.0, err_msg.format('thirst')
    assert result['exhaustion'] == 0.0, err_msg.format('exhaustion')
    assert result['happiness'] == 0.0, err_msg.format('happiness')
