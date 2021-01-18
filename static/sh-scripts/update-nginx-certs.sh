#!/bin/sh

set -e

cd ~/src/ha-docker
tar -C nginx-config -xJf -
sudo docker-compose kill -s HUP nginx
sudo docker-compose kill -s HUP mosquitto
