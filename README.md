A netcat tool written in python3, meant for usage on Linux. WIP. Linux-HaikuOS ( and vice versa ) compatibility and server multi-threading coming soon

# USAGE

## Server
python3 netcat_server.py -t &lt;bind ipv6&gt; -p &lt;bind port&gt; -i &lt;ip version&gt 

## Client
python3 netcat_client.py -t &lt;target ipv6&gt; -p &lt;target port&gt; -i &lt;ip version&gt;
### File transfer 
python3 netcat_server.py -t &lt;target ip&gt; -p &lt;target port&gt; -i &lt;ip version&gt; -c path/to.file
