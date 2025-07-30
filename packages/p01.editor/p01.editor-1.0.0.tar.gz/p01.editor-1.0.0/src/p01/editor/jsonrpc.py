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
from __future__ import unicode_literals
$Id: jsonrpc.py 5352 2025-06-10 15:25:33Z roger.ineichen $
"""
from __future__ import absolute_import

__docformat__ = "reStructuredText"

from p01.jsonrpc.publisher import MethodPublisher

import p01.editor.util


class XEditorPaste(MethodPublisher):
    """Knows how to cleanup any text pasted into XEditor"""

    def doXEditorPaste(self, textBefore, textAfter):
        return p01.editor.util.simpleHTML(textAfter)