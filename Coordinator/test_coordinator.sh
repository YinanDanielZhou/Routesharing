#!/bin/zsh

# ip_prefix="192.168."
# ip_suffix_array=("0.0" "0.1" "0.2" "0.3" "0.4" "0.5" "0.6" "0.7" "0.8" "0.9")

# for ip_suffix in ${ip_suffix_array[@]}
# do
#     ip="$ip_prefix$ip_suffix"
#     # ip="0"
#     for port in 10000 20000
#     do
#         curl -4 -X POST -H "Content-Type: application/json" -d '{"ip": "'$ip'", "port": '"$port"'}' localhost:5000/server/register
#     done
# done


# compensation_choices= {5..50..5}
# frequency_choices= {1..10..2}
# compensation=5
# frequency=1
# server_quantity=2
# curl -4 -X POST -H "Content-Type: application/json" -d '{"compensation": '$compensation', "frequency": '$frequency', "server_quantity": '$server_quantity'}' localhost:5000/consumer/register

