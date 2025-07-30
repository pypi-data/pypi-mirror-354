##############################################################################
#
# Copyright (c) 2007 Projekt01 GmbH and Contributors.
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
$Id: __init__.py 6 2006-04-16 01:28:45Z roger.ineichen $
"""

from __future__ import absolute_import
import zope.interface
from zope.interface import implementer

from z3c.template.template import getLayoutTemplate
from z3c.template.template import getPageTemplate

from j01.jsonrpc import jspage
from j01.dialog import interfaces


@implementer(interfaces.IDialogPage)
class DialogPage(jspage.JSONRPCPage):
    """Simple dialog page."""


    layout = getLayoutTemplate(name='dialog')
    template = getPageTemplate()

    j01DialogTitle = None
    contentTargetExpression = None
    closeDialog = False
    nextURL = None

    def renderClose(self):
        """Return content if you need to render content after close."""
        return None


@implementer(interfaces.IDialogIFrame)
class DialogFrame(DialogPage):
    """Dialog with an IFrame."""


    template = getPageTemplate(name='iframe')

    iFramePageName = None

    @property
    def iFrameURL(self):
        return '%s/%s' % (self.contextURL, self.iFramePageName)

    def __call__(self):
        """update render"""
        # render iframe dialog, nothing else
        return self.template()
