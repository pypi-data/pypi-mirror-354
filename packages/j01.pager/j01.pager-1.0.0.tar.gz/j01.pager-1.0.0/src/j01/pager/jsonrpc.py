##############################################################################
#
# Copyright (c) 2007 Projekt01 GmbH.
# All Rights Reserved.
#
##############################################################################
"""
from __future__ import unicode_literals
$Id: member.py 462 2007-05-14 05:15:55Z roger.ineichen $
"""
from __future__ import absolute_import
__docformat__ = "reStructuredText"

from zope.security.proxy import removeSecurityProxy

from z3c.template.template import getPageTemplate

from p01.jsonrpc.publisher import MethodPublisher

import j01.pager.browser


class J01PagerResult(j01.pager.browser.J01PagerCore, MethodPublisher):
    """JSON live search method with template for rendering the result."""

    def getJ01PagerResult(self, page, batchSize=None, sortName=None,
        sortOrder=None, searchString=None):
        """Returns the search result as JSON data.

        The returned value provides the following data structure:

        return {'content': 'result content'}

        Where the key/values are:

        content: a list of items represented as html content.

        Note: this class uses an named and not an unnamed template called
        j01Pager.
        Normaly you will register this j01Pager template for the mixin class
        shared within your J01Pager page or form.

        """
        # update additional pager data
        self.j01PagerUpdate()
        # setup pager batch data
        self.setUpJ01PagerBatchData(page, batchSize, sortName, sortOrder,
            searchString)

        # return pager batch data as content
        return {'content': self.j01Pager}
