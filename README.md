A "netcat" ( somehwat misleading name, since it provides different base functionality than the UNIX netcat does ) tool written in python3, meant for usage on Linux. Currently features a very basic remote shell and file transfer. WIP. Linux-HaikuOS ( and vice versa ) compatibility, AES encryption and server multi-threading coming soon

# USAGE
![(usage gif)](https://i.imgur.com/fmzZc3E.gif)

## Server
python3 netcat_server.py -t &lt;bind ipv6&gt; -p &lt;bind port&gt; -i &lt;ip version&gt 

## Client
python3 netcat_client.py -t &lt;target ipv6&gt; -p &lt;target port&gt; -i &lt;ip version&gt;
### File transfer 
python3 netcat_server.py -t &lt;target ip&gt; -p &lt;target port&gt; -i &lt;ip version&gt; -c path/to.file
