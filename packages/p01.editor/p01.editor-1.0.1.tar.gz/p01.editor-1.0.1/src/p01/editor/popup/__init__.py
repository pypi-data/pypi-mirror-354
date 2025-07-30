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
"""
$Id: __init__.py 5352 2025-06-10 15:25:33Z roger.ineichen $
"""

from __future__ import unicode_literals
from __future__ import absolute_import

import j01.dialog.jspage


class LinkPage(j01.dialog.jspage.DialogPage):
    """Link insert page"""

class FlashPage(j01.dialog.jspage.DialogPage):
    """Flash insert page"""


class MediaPage(j01.dialog.jspage.DialogPage):
    """Media insert page"""


class PastePage(j01.dialog.jspage.DialogPage):
    """Paste content page"""
