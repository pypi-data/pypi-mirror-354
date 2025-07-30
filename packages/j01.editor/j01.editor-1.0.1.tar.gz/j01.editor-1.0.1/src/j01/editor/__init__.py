###############################################################################
#
# Copyright (c) 2014 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Widgt mixin classes shared in form and jsform

$Id: __init__.py 5222 2025-04-09 08:48:29Z rodrigo.ristow $
"""
from __future__ import absolute_import
from __future__ import unicode_literals

from xml.sax import saxutils

import six


def escape(value):
    """Escape the given value"""
    if isinstance(value, six.string_types):
        value = saxutils.escape(value)
    return value