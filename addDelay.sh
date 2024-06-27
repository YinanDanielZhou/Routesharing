for i in {1..20}
do
    docker exec -it s$i-web-1 tc qdisc add dev eth0 root netem delay 20ms
done
