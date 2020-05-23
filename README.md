[![Build Status](https://travis-ci.org/YarivLevy81/Anthon.svg?branch=master)](https://travis-ci.org/github/YarivLevy81/Anthon)
[![codecov](https://codecov.io/gh/YarivLevy81/Anthon/branch/master/graph/badge.svg)](https://codecov.io/gh/YarivLevy81/Anthon)

# Final Project at Advanced System Design course, TAU

## Installation

1. Clone the repository:

    ```console
    $ git clone https://github.com/YarivLevy81/Anton.git
    $ cd Anton/
    ```

2. Run installation, acitvate environment:

    ```console
    $ ./scripts/install.sh
    $ source .env/bin/activate
    .AntonEnv >
    ```

## Interfaces

**1. Client** - upload samples to the server (assumes .mind file type)

```python
>>> from Anton.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gzip')
...
```
    
errno | -
------------ | -------------
-2 | File 'path' doesn't exist
-3 | File 'path' isn't .gz type
-4 | Server at 'host':'port' issue
    
**2. Server** - run server that forwards snapshots to other components,
   publish can also be a function
   
```python
>>> from Anton.server import run_server
>>> run_server(host='127.0.0.1', port=8000, publish="rabbitmq://127.0.0.1:5672") # publish to RabbitMQ
>>> run_server(host='127.0.0.1', port=8000, publish=print) # print the message
...
```
    
errno | -
------------ | -------------
-2 | Can't bind server to 'host':'port'
-3 | provided publisher isn't supported

**3. Parsers** - run parser of some type, publishing result if needed
```python
>>> from Anton.parsers import run_parser
>>> from Anton.parsers import parse
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
    
errno | -
------------ | -------------
-2 | Parser type unknown
-3 | File 'path' doesn't exist
-4 | File 'path' formatted (see above)
-5 | provided publisher isn't supported


4. **Saver** - run saver (currently only MongoDB supported), integrated with RabbitMQ
```python
>>> from Anton.saver import run_saver
>>> from Anton.saver import saver
>>> ...
>>> database = 'mongodb://127.0.0.1:27017'
>>> topic = 'pose'
>>> path = '/data/pose.result'
>>> publisher = 'rabbitmq://127.0.0.1:5672'
>>> ...
>>> save(database=database, topic=topic, path=path)
>>> run_saver(database=database, publisher=publisher) # Currently only MongoDB (database), RabbitMQ (publisher) are supported
```

.result files are similar to mentioned above. 

errno | -
------------ | -------------
-2 | File 'path' doesn't exist
-3 | File 'path' formatted (see above)
-4 | provided publisher/database aren't supported

5. **API** - run Anton's RESTFUL-API.

```python
>>> from Anton.api import run_server
>>> run_server(host='127.0.0.1', port=5000, database="mongodb://127.0.0.1:27017")
... # Only MongoDB is currently supported
```

errno | -
------------ | -------------
-2 | Can't bind api to 'host':'port'

6. **GUI** - run Anton's GUI.

```python
>>> from Anton.gui import run_server
>>> run_server(
...     host='127.0.0.1',
...     port=8080,
...     api_host='127.0.0.1'.
...     api_port=5000
...)
```

The GUI assumes a running API server (see section 5) in api_host:api_port.

errno | -
------------ | -------------
-2 | Can't bind gui-server to 'host':'port'


## CLI

The following are supported - 
```python
    $ python -m Anton.cli get-users
    … # JSON Array with users is returned
    … [{"user_id": 1, "username": "Barak Obama"}]
    
    $ python -m Anton.cli get-user 1
    … # The parameter is the user_id 
    … {"user_id": 1, "username": "Barak Obama", "birthdate": 12345678, "gender": 0}
    
    $ python -m Anton.cli get-snapshots 1
    … # JSON Array with snapshots are returned (empty if no users inserted), The parameter is the user_id
    … [{"snapshot_id": "6162e82630e1454d92f65b105ad75042", "timestamp": 1575446887339}, {"snapshot_id": "b7d510d93ce74b6e94a06a3e84c9926c", "timestamp": 1575446887412}, {"snapshot_id": "abd32178bd8343db869ab1386319bb8e", "timestamp": 1575446887476}]
    
    $ python -m Anton.cli get-snapshot 1 2
    … # The parameters are user_id and snapshot_id
    … {"snapshot_id": "6162e82630e1454d92f65b105ad75042", "timestamp": 1575446887339, "pose": {"translation_x": 0.4873843491077423, "translation_y": 0.007090016733855009, ... }}
    
    $ python -m Anton.cli get-result 1 2 'pose'
    … # The parameters are user_id, snapshot_id an parser_type
    … {"translation_x": 0.4873843491077423, "translation_y": 0.007090016733855009, "translation_z": -1.1306129693984985, "rotation_x": -0.10888676356214629, "rotation_y": -0.26755994585035286, "rotation_z": -0.021271118915446748, "rotation_w": 0.9571326384559261}
```
    
For each of the commands, an empty JSON Object/Array will be returned on failure.

## REST-API

Default API host:port is '127.0.0.1':5000.

The following are supported - 

**`GET /users`**

    $ curl -i -H 'Accept: application/json' http://127.0.0.1:5000/users

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 43
    Server: Werkzeug/0.16.0 Python/3.8.2
    Date: Wed, 13 May 2020 14:57:09 GMT

    [{"user_id": 420666777420, "username": "Yariv Levy"}]

**`GET /users/<user_id>`**

    $ curl -i -H 'Accept: application/json' http://127.0.0.1:5000/users/420666777420

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 43
    Server: Werkzeug/0.16.0 Python/3.8.2
    Date: Wed, 13 May 2020 14:57:09 GMT

    {"user_id": 420666777420, "username": "Yariv Levy", "birthdate": 12345678, "gender": 0}

**`GET /users/<user_id>/snapshots`**

    $ curl -i -H 'Accept: application/json' http://127.0.0.1:5000/users/420666777420/snapshots

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 43
    Server: Werkzeug/0.16.0 Python/3.8.2
    Date: Wed, 13 May 2020 14:57:09 GMT

    [{"snapshot_id": "6162e82630e1454d92f65b105ad75042", "timestamp": 1575446887339}, {"snapshot_id": "b7d510d93ce74b6e94a06a3e84c9926c", "timestamp": 1575446887412}, {"snapshot_id": "abd32178bd8343db869ab1386319bb8e", "timestamp": 1575446887476}]
    
**`GET /users/<user_id>/snapshots/<user_id>`**

    $ curl -i -H 'Accept: application/json' http://127.0.0.1:5000/users/420666777420/snapshots/6162e82630e1454d92f65b105ad75042

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 43
    Server: Werkzeug/0.16.0 Python/3.8.2
    Date: Wed, 13 May 2020 14:57:09 GMT

    {"snapshot_id": "6162e82630e1454d92f65b105ad75042", "timestamp": 1575446887339, "pose": {"translation_x": 0.4873843491077423, "translation_y": 0.007090016733855009, "translation_z": -1.1306129693984985, "rotation_x": -0.10888676356214629, "rotation_y": -0.26755994585035286, "rotation_z": -0.021271118915446748, "rotation_w": 0.9571326384559261}, "feelings": {"hunger": 0.0, "thirst": 0.0, "exhaustion": 0.0, "happiness": 0.0}, "depth_image": {"height": 1080, "width": 1920, "image_path": "/users_data/42/6162e82630e1454d92f65b105ad75042/depth_image.png"}, "color_image": {"height": 1080, "width": 1920, "image_path": "/users_data/42/6162e82630e1454d92f65b105ad75042/color_image.png"}}

**`GET /users/<user_id>/snapshots/<user_id>/<result_id>`**

    $ curl -i -H 'Accept: application/json' http://127.0.0.1:5000/users/420666777420/snapshots/6162e82630e1454d92f65b105ad75042/pose
    
    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 43
    Server: Werkzeug/0.16.0 Python/3.8.2
    Date: Wed, 13 May 2020 14:57:09 GMT

    {"translation_x": 0.4873843491077423, "translation_y": 0.007090016733855009, "translation_z": -1.1306129693984985, "rotation_x": -0.10888676356214629, "rotation_y": -0.26755994585035286, "rotation_z": -0.021271118915446748, "rotation_w": 0.9571326384559261}

## Web App

Default host:path => **0.0.0.0:8080**

- [Main page](http://0.0.0.0:8080/) - shows all users in the system
- [User page](http://0.0.0.0:8080/users/42) - shows description of user with links to snapshots
- [Snapshot page](http://0.0.0.0:8080/users/42/snapshots/covfefedeadbeef123) - shows data of snapshot

## Pipeline and Docker

Run pipeline with docker-compose
```console
.AntonEnv > docker-compose -f ./docker/docker-compose.yaml up --build
... --build is optional
```

Run pipeline with .sh script ('encapsulated' docker-compose)
```console
.AntonEnv > ./scripts/run.sh
```

You can run this to reset all Anton's databases and files (this assumes currently running environment with docker-compose)
```console
.AntonEnv > ./scripts/reset.sh
```

## Testing

You can run all unittests with the following command:
```console
.AntonEnv > pytest ./tests/
```
