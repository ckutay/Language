# Aboriginal Language Toolkit (ALTK)
#
# Copyright (C) 2007-2008 University of New South Wales
# Authors: Cat Kutay <ckutay@cse.unsw.edu.au>
#          Alistair McCleod <>
# URL:     http://www.bibli.org.au/
# For license information, see LICENSE.TXT

"""
altk -- the aboriginal language Toolkit -- is a added to NLTK, a suite of open source
Python modules, data sets and tutorials supporting research and
development in natural indigneous language processing.

@version: 0.1.2
"""

##//////////////////////////////////////////////////////
##  Metadata
##//////////////////////////////////////////////////////

# Version.  For each new release, the version number should be updated
# here and in the Epydoc comment (above).
__version__ = "0.1.2"

# Copyright notice
__copyright__ = """\
Copyright (C) 2007-2008 University of New South Wales.

Distributed and Licensed under provisions of the GNU Public
License, which is included by reference.
"""

__license__ = "GNU Public License"
# Description of the toolkit, keywords, and the project's primary URL.
__longdescr__ = """\
Uses the Natural Language Toolkit (NLTK) - a Python package for
processing natural language text.  NLTK requires Python 2.4 or higher."""
__keywords__ = ['NLP', 'CL', 'natural language processing',
                'computational linguistics', 'parsing', 'tagging',
                'tokenizing', 'syntax', 'linguistics', 'language',
                'natural language']
__url__ = "http://www.bilbi.org.au/"

# Maintainer, contributors, etc.
__maintainer__ = "Cat Kutay"
__maintainer_email__ = "ckutay@cse.unsw.edu.au"
__author__ = __maintainer__
__author_email__ = __maintainer_email__

# Import top-level functionality into top-level namespace
from dictionary import *
from tagger import *
from stemmer import *
import sys, nltk, re, pprint # NLTK and related modules -- are these all needed?




