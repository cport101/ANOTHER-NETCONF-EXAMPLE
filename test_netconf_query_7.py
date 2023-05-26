#!/usr/bin/env python3
"""
##########################
# test_netconf_query_7.py
##########################

Retrieve AXOS runniung via netconf.

"""
import logging
from logging.config import dictConfig
from collections import defaultdict
from getpass import getpass as gp
from ncclient import manager
from ncclient.xml_ import to_ele


###############################################################################
# START INPUT VARIABLES
###############################################################################
DEVICE_DICT = {
    'host': input('Enter target E9 hostname or ipaddr: '),
    'user': input('Enter netconf_ssh login username: '),
    'password': gp('Enter netconf_ssh login password: '),
    'port': int(input('Enter netconf_ssh port [hit return for port 830]: ') or "830")
}
###############################################################################
# END INPUT VARIABLES
###############################################################################

###############################################################################
# VARIABLES
###############################################################################

RPC_COPY_CONFIG_0 = """
<upload-config-file xmlns="http://www.calix.com/ns/exa/base">
<location>1/1</location>
<vrf>MGMT</vrf>
<from-file>startup-config.xml</from-file>
<to-URI>scp://user_bogus@bogus_server//home/user_bogus/Calix_Test.xml</to-URI>
<password>bogus123</password>
</upload-config-file>
"""


###############################################################################
# FUNCTION [0] TO SETUP LOGGING
###############################################################################
def init_logger():
    """
    DEFINE LOGGER FUNCTIONS
    """
    logging_config = dict(
        version=1,
        formatters={
            "format_f": {
                "format": "%(asctime)s %(name)-10s %(levelname)-6s %(message)s"
            }
        },
        handlers={
            "handler_h": {
                "class": "logging.StreamHandler",
                "formatter": "format_f",
                #"level": logging.INFO,
                "level": logging.DEBUG,
            }
        },
        root={
            "handlers": ["handler_h"],
            "level": logging.DEBUG,
        },
    )
    dictConfig(logging_config)
    logger = logging.getLogger()
    #logging.getLogger("netmiko").setLevel(logging.WARNING)
    logging.getLogger("ncclient").setLevel(logging.DEBUG)
    if logger:
        return True


###############################################################################
# FUNCTION [1]
###############################################################################
def netconf_connect(net_info):
    """
    Est. Netconf via SSH connection to target. The external ncclient library
    is used for creating this connection.
    ----------------
    Expecting a dict
    """
    axos_conn = manager.connect(host=net_info['host'],
                                    username=net_info['user'],
                                    password=net_info['password'],
                                    port=net_info['port'],
                                    hostkey_verify=False,
                                    allow_agent=False,
                                    look_for_keys=False,
                                    timeout = 120)
    if axos_conn.connected:
        logging.info('{0} connected'.format(net_info['host']))
        return axos_conn


###############################################################################
# MAIN
###############################################################################
def main():
    """
    MAIN
    """
    # Call the logger
    rpc_reply = ''
    file_zer0 = '/tmp/config.xml'
    start_logging = init_logger()
    if start_logging:
        logging.info("Ncclient script is starting.")
    with netconf_connect(DEVICE_DICT) as axos_query:
        logging.info('Targetting netconf host {0}'.format(DEVICE_DICT['host']))
        logging.info('Sending rpc: {0}'.format(RPC_COPY_CONFIG_0))
        try:
            rpc_reply = axos_query.dispatch(to_ele(RPC_COPY_CONFIG_0))
            if rpc_reply:
                logging.info("RPC/netconf got a reply")
                logging.info(f"RPC reply: {rpc_reply}")
                logging.info("Writing response to file")
                with open((file_zer0), "w", encoding='UTF-8') as f_0:
                    f_0.write(str(rpc_reply))
                    f_0.close()
        except Exception as sessionException:
            print("An exception occurred while closing the session :" + str(sessionException))


if __name__ == '__main__':
    main()
