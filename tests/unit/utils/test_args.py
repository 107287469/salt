# -*- coding: utf-8 -*-

# Import python libs
from __future__ import absolute_import

# Import Salt Libs
from salt.utils import args

# Import Salt Testing Libs
from salttesting import TestCase, skipIf
from salttesting.mock import NO_MOCK, NO_MOCK_REASON


@skipIf(NO_MOCK, NO_MOCK_REASON)
class ArgsTestCase(TestCase):
    '''
    TestCase for salt.utils.test_args module
    '''

    def test_condition_input_string(self):
        '''
        Test passing a jid on the command line
        '''
        cmd = args.condition_input(['*', 'foo.bar', 20141020201325675584], None)
        self.assertIsInstance(cmd[2], str)