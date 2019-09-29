#!/bin/bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with  :"
    echo "  $0 $*"
    exit 1
fi

set -e

apt update -y &&   apt upgrade -y
apt -y install python3 python3-pip python3-dev python3-systemd #python3-requests
pip3 install pipenv
pipenv install 

cp tweet.py /usr/local/bin/tweet.py
chmod +x /usr/local/bin/tweet.py

tee /etc/systemd/system/tweet.service > /dev/null <<EOT
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
systemctl enable tweet.service
systemctl start tweet.service

echo "Install complete"
