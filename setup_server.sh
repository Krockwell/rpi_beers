#!/bin/bash
sudo http-server -p 80 &
python ../rpi_beers/thermometer.py &

