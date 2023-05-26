# ANOTHER NETCONF AXOS (E9) EXAMPLE

Another ncclient example -- I found that to "send" and RPC 'command', we needed to use the "from ncclient.xml_ import to_ele" -- so the key were these lines:

    with netconf_connect(DEVICE_DICT) as axos_query:
        logging.info('Targetting netconf host {0}'.format(DEVICE_DICT['host']))
        logging.info('Sending rpc: {0}'.format(RPC_COPY_CONFIG_0))
        try:
            rpc_reply = axos_query.dispatch(to_ele(RPC_COPY_CONFIG_0))  #KEY -- use dispatch + to_ele 


Here is the output from the script as it ran:

# Script OUTPUT 


<pre> 
bogus@test-srv4:~/PY$ ./test_netconf_query_7.py 
Enter target E9 hostname or ipaddr: nuat2
Enter netconf_ssh login username: bogus0
Enter netconf_ssh login password: 
Enter netconf_ssh port [hit return for port 830]: 
2023-05-26 16:35:08,038 root       INFO   Ncclient script is starting.
2023-05-26 16:35:09,035 root       INFO   nuat2 connected
2023-05-26 16:35:09,035 root       INFO   Targetting netconf host uat2
2023-05-26 16:35:09,035 root       INFO   Sending rpc: 
</pre>

```xml
<upload-config-file xmlns="http://www.calix.com/ns/exa/base">
<location>1/1</location>
<vrf>MGMT</vrf>
<from-file>startup-config.xml</from-file>
<to-URI>scp://bogus@192.168.254.254//home/bogus/Calix_Test.xml</to-URI>
<password>test123</password>
</upload-config-file>
```


 
<pre>
2023-05-26 16:35:09,221 root       INFO   RPC/netconf got a reply
2023-05-26 16:35:09,221 root       INFO   RPC reply: <?xml version="1.0" encoding="UTF-8"?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:e05c2db0-550d-416a-8638-8b22a08d12e4" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"><status xmlns='http://www.calix.com/ns/exa/base'>Initiating upload</status>
</rpc-reply>
2023-05-26 16:35:09,221 root       INFO   Writing response to file
bogus@test-srv4:~/PY$ 
</pre>

The output from the CALIX e-9 CLX3001


# E9-OUTPUT

<pre>
 SECURITY EVENT 101 'user-login' at 05-26-2023 15:36:55/config/system/aaa/user[name='bogus0']  
 GENERAL EVENT 2401 'transfer-requested' at 05-26-2023 15:36:55/config/system  
 SECURITY EVENT 102 'user-logout' at 05-26-2023 15:36:55/config/system/aaa/user[name='bogus0']  
 GENERAL EVENT 2406 'config-file-copied' at 05-26-2023 15:36:59/config/system  
</pre> 

The confirmation that the file had been uploaded 

# SERVER OUTPUT

<pre>
bogus@test-srv6:~$ ls -la Cal*
-rw-r--r-- 1 bogus bogus 778692 May 26 16:35 Calix_Test.xml
bogus@test-srv6:~$ 
</pre>
