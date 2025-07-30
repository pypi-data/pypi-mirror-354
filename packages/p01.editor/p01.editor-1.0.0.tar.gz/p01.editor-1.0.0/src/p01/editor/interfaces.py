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
$Id: interfaces.py 5352 2025-06-10 15:25:33Z roger.ineichen $
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import zope.schema

import z3c.form.interfaces


class IXEditorWidget(z3c.form.interfaces.ITextAreaWidget):
    """XEditor editor widget"""

    xEditorJavaScript = zope.schema.Field(u"Editor JavaScript")