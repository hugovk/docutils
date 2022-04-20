#! /usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for misc.py "raw" directive.
"""

import unittest

from docutils import frontend
from docutils import utils
from docutils.parsers import rst


class TestRaw(unittest.TestCase):
    def test_raw(self):
        settings = frontend.get_default_settings(rst.Parser)
        settings.report_level = 5
        settings.halt_level = 5
        settings.debug = False
        parser = rst.Parser()

        for casenum, (case_input, case_expected) in enumerate(raw):
            with self.subTest(id=f'raw[{casenum}]'):
                document = utils.new_document('test data', settings.copy())
                parser.parse(case_input, document)
                output = document.pformat()
                self.assertEqual(output, case_expected)


raw = [
["""\
.. raw:: html

   <span>This is some plain old raw text.</span>
""",
"""\
<document source="test data">
    <raw format="html" xml:space="preserve">
        <span>This is some plain old raw text.</span>
"""],
[f"""\
.. raw:: html
   :file: test_parsers/test_rst/test_directives/raw1.txt
""",
f"""\
<document source="test data">
    <raw format="html" source="test_parsers/test_rst/test_directives/raw1.txt" xml:space="preserve">
        <p>This file is used by <tt>test_raw.py</tt>.</p>
"""],
["""\
.. raw:: html
   :file: rawfile.html
   :url: http://example.org/
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            The "file" and "url" options may not be simultaneously specified for the "raw" directive.
        <literal_block xml:space="preserve">
            .. raw:: html
               :file: rawfile.html
               :url: http://example.org/
"""],
["""\
.. raw:: html
   :file: rawfile.html

   <p>Can't have both content and file attribute.</p>
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            "raw" directive may not both specify an external file and have content.
        <literal_block xml:space="preserve">
            .. raw:: html
               :file: rawfile.html
            \n\
               <p>Can't have both content and file attribute.</p>
"""],
[r"""
.. raw:: latex html

   \[ \sum_{n=1}^\infty \frac{1}{n} \text{ etc.} \]
""",
"""\
<document source="test data">
    <raw format="latex html" xml:space="preserve">
        \\[ \\sum_{n=1}^\\infty \\frac{1}{n} \\text{ etc.} \\]
"""],
[f"""\
.. raw:: html
   :file: test_parsers/test_rst/test_directives/utf-16.csv
   :encoding: utf-16
""",
f"""\
<document source="test data">
    <raw format="html" source="test_parsers/test_rst/test_directives/utf-16.csv" xml:space="preserve">
        "Treat", "Quantity", "Description"
        "Albatr\u00b0\u00df", 2.99, "\u00a1On a \u03c3\u03c4\u03b9\u03ba!"
        "Crunchy Frog", 1.49, "If we took the b\u00f6nes out, it wouldn\u2019t be
        crunchy, now would it?"
        "Gannet Ripple", 1.99, "¿On a στικ?"
"""],
[f"""\
Raw input file is UTF-16-encoded, and is not valid ASCII.

.. raw:: html
   :file: test_parsers/test_rst/test_directives/utf-16.csv
   :encoding: ascii
""",
f"""\
<document source="test data">
    <paragraph>
        Raw input file is UTF-16-encoded, and is not valid ASCII.
    <system_message level="4" line="3" source="test data" type="SEVERE">
        <paragraph>
            Problem with "raw" directive:
            UnicodeDecodeError: 'ascii' codec can't decode byte 0xfe in position 0: ordinal not in range(128)
        <literal_block xml:space="preserve">
            .. raw:: html
               :file: test_parsers/test_rst/test_directives/utf-16.csv
               :encoding: ascii
"""],
["""\
.. raw:: html
   :encoding: utf-8

   Should the parser complain becau\xdfe there is no :file:?  BUG?
""",
"""\
<document source="test data">
    <raw format="html" xml:space="preserve">
        Should the parser complain becau\xdfe there is no :file:?  BUG?
"""],
["""\
.. raw:: html
""",
"""\
<document source="test data">
    <system_message level="3" line="1" source="test data" type="ERROR">
        <paragraph>
            Content block expected for the "raw" directive; none found.
        <literal_block xml:space="preserve">
            .. raw:: html
"""],
["""\
.. raw:: html
   :file: non-existent.file
""",
"""\
<document source="test data">
    <system_message level="4" line="1" source="test data" type="SEVERE">
        <paragraph>
            Problems with "raw" directive path:
            InputError: [Errno 2] No such file or directory: 'non-existent.file'.
        <literal_block xml:space="preserve">
            .. raw:: html
               :file: non-existent.file
"""],
]

if __name__ == '__main__':
    unittest.main()
