[![Build Status](https://travis-ci.org/YarivLevy81/Anthon.svg?branch=master)](https://travis-ci.org/github/YarivLevy81/Anthon)
[![codecov](https://codecov.io/gh/YarivLevy81/Anthon/branch/master/graph/badge.svg)](https://codecov.io/gh/YarivLevy81/Anthon)

# Final Project at Advanced System Design course, TAU

## Installation

1. Clone the repository:

    ```sh
    $ git clone https://github.com/YarivLevy81/Anthon.git
    $ cd Anthon/
    ```

2. Run installation, acitvate environment:

    ```sh
    $ ./scripts/install.sh
    $ source .env/bin/activate
    [Anthon] $
    ```

## APIs

1. **Client** - upload sample to the server (assumes .mind file type)
    ```python
    >>> from Anthon.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gzip')
    ...
    ```
2. **Server** - run server that forwards snapshots to other components,
   publish can also be a function
     ```python
    >>> from Anthon.server import run_server
    >>> run_server(host='127.0.0.1', port=8000, publish="rabbitmq://127.0.0.1:5672") # publish to RabbitMQ
    >>> run_server(host='127.0.0.1', port=8000, publish=print) # print the message
    ...
    ```
3. **Parsers** - run parser of some type, publishing result if needed
    ```python
    >>> from Anthon.parsers import run_parser
    >>> from Anthon.parsers import parse
    >>> ...
    >>> parser_type = 'pose'
    >>> data_path = '/snapshots/2da3a844a5f640ce816cd8464e6d77d8.raw'
    >>> publisher = 'rabbitmq://127.0.0.1:5672'
    >>> ...
    >>> parse(parser_type=parser_type, path=data_path)
    >>> run_praser(parser_type=parser_type, publisher=publisher) # Currently only RabbitMQ publisher is supported
    ```
    parser_type is one of ['pose', 'color_image', 'depth_image', 'feelings'], data_path is a path to a file of the following format - 
    ```json
    {
        "user_id": 420777666420, 
        "username": "Yariv Levy", 
        "birthdate": 123456789, 
        "gender": 0, 
        "snapshot_id": "2da3a844a5f640ce816cd8464e6d77d8", 
        "snapshot_path": "/snapshots/2da3a844a5f640ce816cd8464e6d77d8.snp", 
        "timestamp": 1575446887339
    }
    ```
    result example ('pose') - 
    ```json
    {
        "pose": {
            "translation_x": 0.4873843491077423, 
            "translation_y": 0.007090016733855009, 
            "translation_z": -1.1306129693984985, 
            "rotation_x": -0.10888676356214629, 
            "rotation_y": -0.26755994585035286, 
            "rotation_z": -0.021271118915446748, 
            "rotation_w": 0.9571326384559261
        }, 
        "user_id": 420777666420, 
        "username": "Yariv Levy", 
        "birthdate": 123456789, 
        "gender": 0, 
        "snapshot_id": "2da3a844a5f640ce816cd8464e6d77d8", 
        "snapshot_path": "/snapshots/2da3a844a5f640ce816cd8464e6d77d8.snp", 
        "timestamp": 1575446887339
    }

    ```
4. **Saver** - run saver (currently only MongoDB supported), integrated with RabbitMQ
    ```python
    >>> from Anthon.saver import run_saver
    >>> from Anthon.saver import saver
    >>> ...
    >>> database = 'mongodb://127.0.0.1:27017'
    >>> topic = 'pose'
    >>> path = '/data/pose.result'
    >>> publisher = 'rabbitmq://127.0.0.1:5672'
    >>> ...
    >>> save(database=database, topic=topic, path=path)
    >>> run_saver(database=database, publisher=publisher) # Currently only MongoDB (database), RabbitMQ (publisher) are supported
.result files are similar to mentioned above. 
    
## Testing

You can run all unittests with the following command:
```sh
$ pytest tests/
```
