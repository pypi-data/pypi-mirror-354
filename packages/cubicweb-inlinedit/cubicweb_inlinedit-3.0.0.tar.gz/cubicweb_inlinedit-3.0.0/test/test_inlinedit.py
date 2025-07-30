# copyright 2011-2024 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

"""cubicweb-inlinedit automatic tests"""
from cubicweb_web.devtools.testlib import AutomaticWebTest


class AutomaticWebTest(AutomaticWebTest):
    """provides `to_test_etypes` and/or `list_startup_views` implementation
    to limit test scope
    """


if __name__ == "__main__":
    import unittest

    unittest.main()
