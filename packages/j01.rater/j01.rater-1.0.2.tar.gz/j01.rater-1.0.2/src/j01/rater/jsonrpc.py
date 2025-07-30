##############################################################################
#
# Copyright (c) 2007 Zope Foundation and Contributors.
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
$Id: views.py 93 2006-07-22 22:57:31Z roger.ineichen $
"""
from __future__ import absolute_import

__docformat__ = 'restructuredtext'

import zope.component
import zope.interface
from zope.interface import implementer
from zope.authentication.interfaces import IUnauthenticatedPrincipal

from z3c.form.interfaces import IForm

from p01.jsonrpc.interfaces import IJSONRPCPublisher
from p01.jsonrpc.interfaces import IJSONRPCRequest
from p01.jsonrpc.publisher import MethodPublisher

from j01.rater import interfaces


@implementer(IJSONRPCPublisher)
class J01Rater(MethodPublisher):
    """JSON-RPC rater methods"""

    zope.component.adapts(IForm, IJSONRPCRequest)

    def j01Rater(self, fieldName, key):
        """Apply rating to the right field for logged in users."""
        content = None

        # setup widget
        self.context.fields = self.context.fields.select(fieldName)
        self.context.updateWidgets()
        widget = self.context.widgets.get(fieldName)
        if not IUnauthenticatedPrincipal.providedBy(self.request.principal) \
            and widget is not None:
            # rate if authenticated and we found the widget
            ratingConverter = widget.converter
            pid = self.request.principal.id
            if key == interfaces.CANCEL_RATING_KEY:
                changed = ratingConverter.remove(pid)
            else:
                changed = ratingConverter.rate(pid, key)
            if changed:
                # update and return the widget
                widget.update()
                content = widget.render()

        return {'content':content}
