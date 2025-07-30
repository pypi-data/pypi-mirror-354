##############################################################################
#
# Copyright (c) 2011 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
$Id: jsonrpc.py 5358 2025-06-10 15:57:02Z roger.ineichen $
"""
from __future__ import absolute_import
__docformat__ = 'restructuredtext'

import zope.component
import zope.interface
from zope.interface import implementer
from zope.publisher.interfaces.browser import IBrowserPage

from p01.jsonrpc.publisher import MethodPublisher
from p01.jsonrpc.interfaces import IJSONRPCRequest

from j01.autosuggest import interfaces


@implementer(interfaces.IJSONAutoSuggest)
class FormAutoSuggest(MethodPublisher):
    """Auto suggest JSON-RPC method
    
    NOTE:
    This method is only used for FormAutoSuggestWidget. You must implement
    your own j01AutoSuggest JSON-RPC method if you use the form context or site
    as your j01AutoSuggest method context

    """

    zope.component.adapts(IBrowserPage, IJSONRPCRequest)

    def j01AutoSuggest(self, fieldName, searchString):
        """Retruns an auto suggest result"""
        # setup single widget
        self.context.fields = self.context.fields.select(fieldName)
        self.context.updateWidgets()
        widget = self.context.widgets.get(fieldName)

        items = []
        if widget is not None:
            items = widget.items
        return {'items': items}
