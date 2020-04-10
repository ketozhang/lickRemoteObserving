import os
import logging
import getpass
from lick_vnc_launcher import create_logger, LickVncLauncher, create_parser
import pytest

# create lvl object
create_logger()
lvl = LickVncLauncher()
lvl.log = logging.getLogger('KRO')
lvl.log_system_info()
lvl.args = create_parser()
lvl.get_config()
lvl.check_config()

servers_and_results = [('shimmy', 'shimmy.ucolick.org'),
                       ('noir', 'noir.ucolick.org')
                           ]

def test_vncviewer():
    lvl.log.info('Testing config file: vncviewer')
    vncviewer = lvl.config.get('vncviewer', None)
    if vncviewer in [None, '', 'vncviewer']:
        # the line below will throw and error if which fails
        vncviewer = subprocess.check_output(['which', 'vncviewer'])
    if vncviewer != 'open':
        assert os.path.exists(vncviewer)
    

def test_ssh_key():
    lvl.log.info('Testing config file: ssh_pkey')
    lvl.tel = 'shane'
    lvl.validate_ssh_key()
    assert lvl.ssh_key_valid is True


@pytest.mark.parametrize("server,result", servers_and_results)
def test_connection_to_servers(server, result):

    vnc_account = lvl.ssh_account
    vnc_password = None

    lvl.log.info(f'Testing SSH to {vnc_account}@{server}.ucolick.org')
    output = lvl.do_ssh_cmd('hostname', f'{server}.ucolick.org',
                            vnc_account)
    assert output is not None
    assert output != ''
    assert output.strip() in [server, result]
    lvl.log.info(f' Passed')
