#!/bin/bash

duration=$1
interval=$2

total_encoder=0
total_decoder=0
total_fps=0
total_latency=0
count=0

end_time=$(($(date +%s) + duration))

while [ $(date +%s) -lt $end_time ]; do
    stats=$(nvidia-smi -a | grep -A 5 Encoder)

    encoder=$(echo "$stats" | grep "Encoder" | awk '{print $3}' | tr -d ' %')
    decoder=$(echo "$stats" | grep "Decoder" | awk '{print $3}' | tr -d ' %')
    fps=$(echo "$stats" | grep "Average FPS" | awk '{print $4}')
    latency=$(echo "$stats" | grep "Average Latency" | awk '{print $4}')

    total_encoder=$(echo "$total_encoder + $encoder" | bc -l)
    total_decoder=$(echo "$total_decoder + $decoder" | bc -l)
    total_fps=$(echo "$total_fps + $fps" | bc -l)
    total_latency=$(echo "$total_latency + $latency" | bc -l)

    count=$((count + 1))

    sleep $interval
done

average_encoder=$(echo "scale=2; $total_encoder / $count" | bc -l)
average_decoder=$(echo "scale=2; $total_decoder / $count" | bc -l)
average_fps=$(echo "scale=2; $total_fps / $count" | bc -l)
average_latency=$(echo "scale=2; $total_latency / $count" | bc -l)

echo "Average Encoder: $average_encoder%"
echo "Average Decoder: $average_decoder%"
echo "Average FPS: $average_fps"
echo "Average Latency: $average_latency"