#!/usr/bin/gnuplot
set terminal png
set term pngcairo size 800,600
set output "../images/graph_p1.png"
set title "Probe 1"
set xlabel "Time"
set ylabel "Temperature (F)"
set yrange [40:60]
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%H:%M"
set grid xtics lc rgb "#888888" lw 1 lt 0
set grid ytics lc rgb "#888888" lw 1 lt 0
plot "../logs/temperature_p1.log" using 1:3 title "temperature" with lines lc rgb '#8b1a0e' lt 1 lw 2
