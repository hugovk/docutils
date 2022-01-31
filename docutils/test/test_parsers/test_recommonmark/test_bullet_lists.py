#!/usr/bin/env python3
# :Copyright: © 2020 Günter Milde.
# :License: Released under the terms of the `2-Clause BSD license`_, in short:
#
#    Copying and distribution of this file, with or without modification,
#    are permitted in any medium without royalty provided the copyright
#    notice and this notice are preserved.
#    This file is offered as-is, without any warranty.
#
# .. _2-Clause BSD license: https://opensource.org/licenses/BSD-2-Clause

"""
Test for bullet lists in CommonMark parsers.
Cf. the `CommonMark Specification <https://spec.commonmark.org/>`__
"""

import unittest

from docutils import frontend
from docutils import utils
import docutils.parsers

md_parser_class = docutils.parsers.get_parser_class('recommonmark')


class TestRecommonmarkBulletLists(unittest.TestCase):
    def test_bullet_lists(self):
        parser = md_parser_class()
        settings = frontend.get_default_settings(md_parser_class)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False

        for casenum, (case_input, case_expected) in enumerate(bullet_lists):
            with self.subTest(id=f'bullet_lists[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


bullet_lists = [
["""\
- item
""",
"""\
<document source="test data">
    <bullet_list>
        <list_item>
            <paragraph>
                item
"""],
["""\
* item 1

* item 2
""",
"""\
<document source="test data">
    <bullet_list>
        <list_item>
            <paragraph>
                item 1
        <list_item>
            <paragraph>
                item 2
"""],
["""\
No blank line between:

+ item 1
+ item 2
""",
"""\
<document source="test data">
    <paragraph>
        No blank line between:
    <bullet_list>
        <list_item>
            <paragraph>
                item 1
        <list_item>
            <paragraph>
                item 2
"""],
["""\
- item 1, paragraph 1.

  item 1, paragraph 2.

- item 2
""",
"""\
<document source="test data">
    <bullet_list>
        <list_item>
            <paragraph>
                item 1, paragraph 1.
            <paragraph>
                item 1, paragraph 2.
        <list_item>
            <paragraph>
                item 2
"""],
["""\
- item 1, line 1
  item 1, line 2
- item 2
""",
"""\
<document source="test data">
    <bullet_list>
        <list_item>
            <paragraph>
                item 1, line 1
                item 1, line 2
        <list_item>
            <paragraph>
                item 2
"""],
["""\
Different bullets start different lists:

- item 1

+ item 1

* no blank line
- required between lists
""",
"""\
<document source="test data">
    <paragraph>
        Different bullets start different lists:
    <bullet_list>
        <list_item>
            <paragraph>
                item 1
    <bullet_list>
        <list_item>
            <paragraph>
                item 1
    <bullet_list>
        <list_item>
            <paragraph>
                no blank line
    <bullet_list>
        <list_item>
            <paragraph>
                required between lists
"""],
["""\
- item 1
continuation of item 1
""",
"""\
<document source="test data">
    <bullet_list>
        <list_item>
            <paragraph>
                item 1
                continuation of item 1
"""],
["""\
-

empty item above
""",
"""\
<document source="test data">
    <bullet_list>
        <list_item>
    <paragraph>
        empty item above
"""],
["""\
-
empty item above, no blank line
""",
"""\
<document source="test data">
    <bullet_list>
        <list_item>
    <paragraph>
        empty item above, no blank line
"""],
["""\
Unicode bullets are not supported by CommonMark.

• BULLET

‣ TRIANGULAR BULLET

⁃ HYPHEN BULLET
""",
"""\
<document source="test data">
    <paragraph>
        Unicode bullets are not supported by CommonMark.
    <paragraph>
        • BULLET
    <paragraph>
        ‣ TRIANGULAR BULLET
    <paragraph>
        ⁃ HYPHEN BULLET
"""],
]

if __name__ == '__main__':
    unittest.main()
