#!/bin/bash
python3 -m venv venv || echo "venv already exists";
source venv/bin/activate
pip3 install -r requirements.txt
mkdir resources/music || echo "resources/music already exists";