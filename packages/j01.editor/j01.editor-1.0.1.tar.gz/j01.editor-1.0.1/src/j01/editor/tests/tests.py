###############################################################################
#
# Copyright (c) 2017 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Tests
$Id: tests.py 5222 2025-04-09 08:48:29Z rodrigo.ristow $
"""
from __future__ import absolute_import
from __future__ import print_function

import doctest
import unittest


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('checker.txt',
                             globs={'print_function': print_function,
                                    # 'unicode_literals': unicode_literals,
                                    'absolute_import': absolute_import},
                             ),
        doctest.DocFileSuite('util.txt',
                             globs={'print_function': print_function,
                                    # 'unicode_literals': unicode_literals,
                                    'absolute_import': absolute_import},
                             optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
