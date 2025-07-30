##############################################################################
#
# Copyright (c) 2012 Projekt01 GmbH and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import doctest
import unittest

import six

import z3c.form.testing


def test_suite():
    if six.PY2:
        readme_file = 'README_PY2.txt'
    else:
        readme_file = 'README.txt'
    return unittest.TestSuite((
        doctest.DocFileSuite(readme_file,
                             globs={'print_function': print_function,
                                    'unicode_literals': unicode_literals,
                                    'absolute_import': absolute_import},
                             setUp=z3c.form.testing.setUp,
                             tearDown=z3c.form.testing.tearDown,
                             optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        doctest.DocFileSuite('util.txt',
                             globs={'print_function': print_function,
                                    'unicode_literals': unicode_literals,
                                    'absolute_import': absolute_import},
                             optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
    ))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
