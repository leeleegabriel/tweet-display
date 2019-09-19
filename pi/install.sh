#!/bin/bash

set -e

pip3 install pipenv
pipenv install 

cp run.py /usr/local/bin/tweet.py
chmod +x /usr/local/bin/tweet.py

sudo tee /etc/systemd/system/tweet.service > /dev/null <<EOT
[Unit]
Description=Twitter Alert
After=network.target

[Service]
ExecStart=/usr/bin/python3 -u tweet.py
WorkingDirectory=/usr/local/bin
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOT

sudo systemctl enable tweet.service
sudo systemctl start tweet.service
