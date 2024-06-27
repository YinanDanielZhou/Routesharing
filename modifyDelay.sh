docker exec -it s1-web-1 tc qdisc add dev eth0 root netem delay 100ms
docker exec -it s2-web-1 tc qdisc add dev eth0 root netem delay 100ms
docker exec -it s3-web-1 tc qdisc add dev eth0 root netem delay 100ms
