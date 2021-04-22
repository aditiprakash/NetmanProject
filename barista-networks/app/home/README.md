Before running the listen_to_trap.py, please run the following command on your machine:

sudo iptables -A PREROUTING -t nat -p udp --dport 162 -j REDIRECT --to-port 1620
