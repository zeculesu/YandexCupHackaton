#!/bin/sh
sudo kill `ps -ef| grep input_uvc.so| awk '{print $2}'`

