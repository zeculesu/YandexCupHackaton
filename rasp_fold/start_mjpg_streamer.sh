#!/bin/sh

cd /home/pi/work/mjpg-streamer-master/mjpg-streamer-experimental
sudo sh start.sh &

#sudo kill -9 `ps -ef| grep mjpg_streamer| awk '{print $2}'`



