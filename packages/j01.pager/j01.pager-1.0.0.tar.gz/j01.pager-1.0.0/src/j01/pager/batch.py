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
$Id: batch.py 5197 2025-03-29 19:46:45Z felipe.souza $
"""
from __future__ import division
from __future__ import absolute_import
from builtins import range
from six import string_types
from builtins import object
from past.utils import old_div
import six
from six.moves import range
__docformat__ = "reStructuredText"

from operator import attrgetter
from operator import itemgetter

import zope.interface
from zope.schema.fieldproperty import FieldProperty
from zope.interface.common.sequence import IFiniteSequence
from zope.interface import implementer
from j01.pager import interfaces


def getBatchData(collection, page=1, size=25, sortName=None, sortOrder=False):
    """Returns a batched sequence, current page, total items and page size."""
    # first, get overall total based on query
    total = len(collection)

    # second calculate pages (batches)
    pages = old_div(total,size)
    if pages == 0 or total % size:
        pages += 1

    # as next we approve our page position
    if page > pages:
        # restart with pages number as page which is the last page
        page = pages
        return getBatchData(collection, page, size, sortName, sortOrder)

    # calculate start size
    start = (page-1) * size

    # setup batch
    cursor = Batch(collection, start, size, sortName, sortOrder)
    # return data including probably adjusted page number
    return (cursor, page, pages, total)


@implementer(interfaces.IBatch)
class Batch(object):
    """Batch implementation. See IBatch"""

    start = FieldProperty(interfaces.IBatch['start'])
    size = FieldProperty(interfaces.IBatch['size'])
    end = FieldProperty(interfaces.IBatch['end'])

    def __init__(self, sequence, start=0, size=20, sortName=None,
        sortOrder=False):
        self.sequence = sequence
        self.total = len(sequence)
        self.update(start, size)
        self.sort(sortName, sortOrder)

    def update(self, start, size):
        # adjust start and size
        if self.total == 0:
            self.start = 0
            self.size = 0

        elif start >= self.total:
            self.start = self.total
            self.size = 0

        elif size >= self.total:
            # 5 15 12
            self.start = start
            # size is what is left from start to end
            self.size = self.total - start

        # use given start and size
        else:
            self.start = start
            self.size = size

        # setup end
        if self.total == 0:
            self.end = -1
        else:
            self.end = self.start + self.size - 1

    def skip(self, start):
        """Skip amount of items"""
        self.update(start, self.size)
        return self

    def limit(self, size):
        """Limit result"""
        self.update(self.start, size)
        return self

    def sort(self, sortName=None, sortOrder=None):
        """Sort sequence"""
        if sortOrder in ['0', 'asc', 'false',  False]:
            # support different marker as non reverse sort order marker
            rev = False
        elif sortOrder in ['1', 'desc', 'reverse', 'reversed', 'true',  True]:
            # support different marker as reverse sort order marker
            rev = True
        else:
            # non reverse by default
            rev = False
        self.sortName = sortName
        # try different sort concept
        if isinstance(sortName,  int):
            # sort with item getter (sequence of tuples)
            self.sequence = sorted(self.sequence, key=itemgetter(sortName),
                reverse=rev)
        elif isinstance(sortName,  six.string_types):
            # sort with attrgetter (sequence of items)
            self.sequence = sorted(self.sequence, key=attrgetter(sortName),
                reverse=rev)
        elif sortName is not None:
            # sort with sort key function (sequence of something)
            self.sequence = sorted(self.sequence, key=sortName,
                reverse=rev)
        elif rev:
            # or just reverse
            self.sequence.reverse()
        return self

    def __getitem__(self, key):
        """See zope.interface.common.sequence.IMinimalSequence"""
        if isinstance(key, slice):
            start, stop, step = key.indices(self.size)
            if step != 1:
                raise ValueError('Slicing with step is not supported')
            if stop > self.end:
                stop = self.size
            return [self.sequence[self.start + idx] for idx in range(start, stop)]
        elif key >= self.size:
            raise IndexError('batch index out of range')
        return self.sequence[self.start + key]

    def __iter__(self):
        """See zope.interface.common.sequence.IMinimalSequence"""
        return iter(self.sequence[self.start:self.end +1])

    def __len__(self):
        """See zope.interface.common.sequence.IFiniteSequence"""
        return self.size

    def __contains__(self, item):
        for i in self:
            if item == i:
                return True
        else:
            return False

    def __eq__(self, other):
        return ((self.size, self.start, self.sequence) ==
                (other.size, other.start, other.sequence))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return self.size != 0

    def __repr__(self):
        return '<%s start=%i, size=%i, total=%i>' % (
            self.__class__.__name__, self.start, self.size, self.total)