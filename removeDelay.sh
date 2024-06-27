for i in {1..20}
do
    docker exec -it s$i-web-1 tc qdisc del dev eth0 root netem
done

