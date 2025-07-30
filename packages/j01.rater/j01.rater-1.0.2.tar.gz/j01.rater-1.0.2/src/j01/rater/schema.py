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
from __future__ import unicode_literals
$Id: __init__.py 6 2006-04-16 01:28:45Z roger.ineichen $
"""

from __future__ import absolute_import

import zope.schema
import zope.interface
from zope.interface import implementer
from zope.schema.interfaces import SchemaNotProvided

from j01.rater import interfaces
from j01.rater.rating import FiveStarRatingConverter
from j01.rater.rating import FiveHalfStarRatingConverter
from j01.rater.rating import FiveHalfStarFullRatingConverter


@implementer(interfaces.IRatingField)
class RatingField(zope.schema.Field):
    """Rating manager field."""


    ratingConverterFactory = None

    def _validate(self, value):
        # schema has to be provided by value
        if not interfaces.IRatingConverter.providedBy(value):
            raise SchemaNotProvided



@implementer(interfaces.IFiveStarRatingField)
class FiveStarRatingField(RatingField):
    """Five half star score system rating field."""

    ratingConverterFactory = FiveStarRatingConverter



@implementer(interfaces.IFiveHalfStarRatingField)
class FiveHalfStarRatingField(RatingField):
    """Five half star score system rating field."""

    ratingConverterFactory = FiveHalfStarRatingConverter



@implementer(interfaces.IFiveHalfStarFullRatingField)
class FiveHalfStarFullRatingField(RatingField):
    """Five half star score system rating field with 1-10 ratings."""

    ratingConverterFactory = FiveHalfStarFullRatingConverter
