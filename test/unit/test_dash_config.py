import pytest
import os
import sys
import re
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
os.environ['SENTINEL_ENV'] = 'test'
sys.path.append(os.path.normpath(os.path.join(os.path.dirname(__file__), '../../lib')))
import config
from wolfcoin_config import wolfcoinConfig


@pytest.fixture
def wolfcoin_conf(**kwargs):
    defaults = {
        'rpcuser': 'egirpc',
        'rpcpassword': 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk',
        'rpcport': 29241,
    }

    # merge kwargs into defaults
    for (key, value) in kwargs.items():
        defaults[key] = value

    conf = """# basic settings
testnet=1 # TESTNET
server=1
rpcuser={rpcuser}
rpcpassword={rpcpassword}
rpcallowip=127.0.0.1
rpcport={rpcport}
""".format(**defaults)

    return conf


def test_get_rpc_creds():
    wolfcoin_config = wolfcoin_conf()
    creds = wolfcoinConfig.get_rpc_creds(wolfcoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'egirpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 29241

    wolfcoin_config = wolfcoin_conf(rpcpassword='s00pers33kr1t', rpcport=8000)
    creds = wolfcoinConfig.get_rpc_creds(wolfcoin_config, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'egirpc'
    assert creds.get('password') == 's00pers33kr1t'
    assert creds.get('port') == 8000

    no_port_specified = re.sub('\nrpcport=.*?\n', '\n', wolfcoin_conf(), re.M)
    creds = wolfcoinConfig.get_rpc_creds(no_port_specified, 'testnet')

    for key in ('user', 'password', 'port'):
        assert key in creds
    assert creds.get('user') == 'egirpc'
    assert creds.get('password') == 'EwJeV3fZTyTVozdECF627BkBMnNDwQaVLakG3A4wXYyk'
    assert creds.get('port') == 19998


# ensure wolfcoin network (mainnet, testnet) matches that specified in config
# requires running wolfcoind on whatever port specified...
#
# This is more of a wolfcoind/jsonrpc test than a config test...
