#!/bin/bash
python3 -m venv venv || echo "venv already exists";
source venv/bin/activate
pip3 install -r requirements.txt

# Check Python version and install audioop-lts if 3.13 or higher
python_version=$(python3 --version | cut -d ' ' -f 2)
if [[ $(echo "$python_version 3.13" | awk '{print ($1 >= $2)}') -eq 1 ]]; then
    pip3 install audioop-lts
fi

mkdir resources/music || echo "resources/music already exists";