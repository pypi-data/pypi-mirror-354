# pylint: disable=W0622
"""cubicweb-inlinedit application packaging information"""

modname = "inlinedit"
distname = "cubicweb-inlinedit"

numversion = (3, 0, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
author = "LOGILAB S.A. (Paris, FRANCE)"
author_email = "contact@logilab.fr"
description = "Extension of the `reledit` builtin feature"
web = f"https://forge.extranet.logilab.fr/cubicweb/cubes/{distname}"

__depends__ = {
    "cubicweb": ">= 4.0.0, < 5.0.0",
    "cubicweb-web": ">= 1.4.0",
    "cwtags": ">=1.2.3",
}

__recommends__ = {}

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]
