#!/bin/bash

set -e

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

sudo apt update -y && sudo apt upgrade -y
sudo apt -y install python3-pip python3-dev python3-systemd

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
