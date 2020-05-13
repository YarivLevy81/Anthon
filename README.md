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

1. Client - upload sample to the server (assumes .mind file type)
    ```python
    >>> from Anthon.client import upload_sample
    >>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gzip')
    ...
    ```
2. Server - run server that forwards snapshots to other components,
   publish can also be a function
     ```python
    >>> from Anthon.server import run_server
    >>> run_server(host='127.0.0.1', port=8000, publish="rabbitmq://127.0.0.1:5672") # publish to rabbbit
    >>> run_server(host='127.0.0.1', port=8000, publish=print) # print the message
    ...
    ```
3. Parsers - run parser of some type, publishing result if needed
    ```python
    >>> from Anthon.parsers import run_parser
    >>> from Anthon.parsers import parse
    >>> ...
    >>> parser_type = ...
    >>> data_path = ..
    >>> ...
    >>> run_praser(parser_type=parser_type, path=data_path)
    ```
    parser_type is one of ['pose', 'color_image', 'depth_image', 'feelings'], data_path is a path to a file of the following format - 
    ```json
    xaxa = {}
    ```

## Testing

You can run all unittests with the following command:
```sh
$ pytest tests/
```
