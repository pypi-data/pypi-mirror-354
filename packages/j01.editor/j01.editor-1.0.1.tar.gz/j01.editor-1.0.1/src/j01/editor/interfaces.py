###############################################################################
#
# Copyright (c) 2017 Projekt01 GmbH.
# All Rights Reserved.
#
###############################################################################
"""Interfaces

$Id: interfaces.py 5222 2025-04-09 08:48:29Z rodrigo.ristow $
"""
from __future__ import absolute_import
from __future__ import unicode_literals

import j01.form.interfaces


# editor text
class IEditorWidget(j01.form.interfaces.ITextAreaWidget):
    """Editor widget"""