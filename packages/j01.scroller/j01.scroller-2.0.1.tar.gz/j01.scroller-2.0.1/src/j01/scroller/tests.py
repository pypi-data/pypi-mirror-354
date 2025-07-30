##############################################################################
#
# Copyright (c) 2013 Projekt01 GmbH and Contributors.
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
"""
from __future__ import unicode_literals
$Id: tests.py 5202 2025-04-05 19:13:16Z felipe.souza $
"""
from __future__ import absolute_import
__docformat__ = "reStructuredText"

import doctest
import unittest


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('README.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
        doctest.DocFileSuite('source.txt',
            optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS),
    ))