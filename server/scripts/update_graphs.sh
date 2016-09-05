#!/bin/bash

while true
do
  gnuplot ./generate_graph_p1.sh
  gnuplot ./generate_graph_p2.sh
  sleep 60
done
