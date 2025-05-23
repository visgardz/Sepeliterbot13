#!/bin/bash

set -e
sudo apt update && sudo apt install -y python3 python3-venv python3-pip ffmpeg

BOT_DIR="/opt/video_bot"
sudo mkdir -p $BOT_DIR
sudo chown $USER:$USER $BOT_DIR
cp -r ./* $BOT_DIR/
cd $BOT_DIR

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

SERVICE_FILE="/etc/systemd/system/video_bot.service"
sudo tee $SERVICE_FILE > /dev/null <<EOF
[Unit]
Description=Telegram Video Split Bot
After=network.target

[Service]
User=$USER
WorkingDirectory=$BOT_DIR
ExecStart=/bin/bash -c 'source $BOT_DIR/venv/bin/activate && python3 $BOT_DIR/bot.py & python3 $BOT_DIR/web_dashboard/app.py'
Restart=always

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable video_bot
sudo systemctl start video_bot

echo "Bot dan Dashboard telah dijalankan."
