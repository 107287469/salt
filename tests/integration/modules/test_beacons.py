# -*- coding: utf-8 -*-
'''
    :codeauthor: :email:`Justin Anderson <janderson@saltstack.com>`
'''

# Python Libs
from __future__ import absolute_import
import os

# 3rd-party libs
import pytest

# Salt Libs
from salt.modules import beacons
from salt.exceptions import CommandExecutionError
import integration

beacons.__opts__ = {}

BEACON_CONF_DIR = os.path.join(integration.TMP, 'minion.d')
if not os.path.exists(BEACON_CONF_DIR):
    os.makedirs(BEACON_CONF_DIR)


@pytest.mark.skip_if_not_root
@pytest.mark.destructive_test
class BeaconsAddDeleteTest(integration.ModuleCase):
    '''
    Tests the add and delete functions
    '''
    def test_add_and_delete(self):
        '''
        Test adding and deleting a beacon
        '''
        _add = self.run_function('beacons.add', ['ps', {'apache2': 'stopped'}])
        self.assertTrue(_add['result'])

        # save added beacon
        _save = self.run_function('beacons.save')
        self.assertTrue(_save['result'])

        # delete the beacon
        _delete = self.run_function('beacons.delete', ['ps'])
        self.assertTrue(_delete['result'])

        # save the results
        self.run_function('beacons.save')


@pytest.mark.skip_if_not_root
@pytest.mark.destructive_test
class BeaconsTest(integration.ModuleCase):
    '''
    Tests the beacons execution module
    '''
    def setUp(self):
        try:
            # Add beacon to disable
            self.run_function('beacons.add', ['ps', {'apache2': 'stopped'}])
            self.run_function('beacons.save')
        except CommandExecutionError:
            self.skipTest('Unable to add beacon')

    def tearDown(self):
        # delete added beacon
        self.run_function('beacons.delete', ['ps'])
        self.run_function('beacons.save')

    def test_disable(self):
        '''
        Test disabling beacons
        '''
        # assert beacon exists
        _list = self.run_function('beacons.list', return_yaml=False)
        self.assertIn('ps', _list)

        ret = self.run_function('beacons.disable')
        self.assertTrue(ret['result'])

        # assert beacons are disabled
        _list = self.run_function('beacons.list', return_yaml=False)
        self.assertFalse(_list['enabled'])

        # disable added beacon
        ret = self.run_function('beacons.disable_beacon', ['ps'])
        self.assertTrue(ret['result'])

        # assert beacon ps is disabled
        _list = self.run_function('beacons.list', return_yaml=False)
        self.assertFalse(_list['ps']['enabled'])

    def test_enable(self):
        '''
        Test enabling beacons
        '''
        # assert beacon exists
        _list = self.run_function('beacons.list', return_yaml=False)
        self.assertIn('ps', _list)

        # enable beacons on minion
        ret = self.run_function('beacons.enable')
        self.assertTrue(ret['result'])

        # assert beacons are enabled
        _list = self.run_function('beacons.list', return_yaml=False)
        self.assertTrue(_list['enabled'])

    @pytest.mark.skipif(True, 'Skip until https://github.com/saltstack/salt/issues/31516 problems are resolved.')
    def test_enabled_beacons(self):
        '''
        Test enabled specific beacon
        '''
        # enable added beacon
        ret = self.run_function('beacons.enable_beacon', ['ps'])
        self.assertTrue(ret['result'])

        # assert beacon ps is enabled
        _list = self.run_function('beacons.list', return_yaml=False)
        self.assertTrue(_list['ps']['enabled'])

    def test_list(self):
        '''
        Test lising the beacons
        '''
        # list beacons
        ret = self.run_function('beacons.list', return_yaml=False)
        if 'enabled' in ret:
            self.assertEqual(ret, {'ps': {'apache2': 'stopped'}, 'enabled': True})
        else:
            self.assertEqual(ret, {'ps': {'apache': 'stopped'}})
