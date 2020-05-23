  
#!/bin/bash

set -e
cd "$(dirname "${BASH_SOURCE[0]}")/.."


function main {
    python3 -m virtualenv .AntonEnv
    find .AntonEnv -name site-packages -exec bash -c 'echo "../../../../" > {}/self.pth' \;
    .AntonEnv/bin/pip install -U pip
    .AntonEnv/bin/pip install -r requirements.txt
}


main "$@"