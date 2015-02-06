# Wiradjuri Language Toolkit (WTK)
#
# Copyright (C) 2007-2008 University of New South Wales
# Authors: Cat Kutay <ckutay@cse.unsw.edu.au>
#          Alistair McCleod <>
# URL:     http://www.bibli.org.au/
# For license information, see LICENSE.TXT

# Import top-level functionality into top-level namespace

from altk import *
from dictionary import *
from tagger import *
from stemmer import *
import urllib
import altk

s=sys.argv[1]

t = altk.translate(s)


