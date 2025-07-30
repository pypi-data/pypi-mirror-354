##############################################################################
#
# Copyright (c) 2011 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
$Id: interfaces.py 5358 2025-06-10 15:57:02Z roger.ineichen $
"""
from __future__ import absolute_import
__docformat__ = 'restructuredtext'

from z3c.form.interfaces import ITextWidget

import p01.jsonrpc.interfaces


class IAutoSuggestWidget(ITextWidget):
    """AutoSuggest widget."""
    

class IJSONAutoSuggest(p01.jsonrpc.interfaces.IJSONRPCRequest):
    """JSON-RPC auto suggest method."""

    def j01AutoSuggest(fieldName, searchString, page, batchSize):
        """Returns the auto suggest result on the search string."""
