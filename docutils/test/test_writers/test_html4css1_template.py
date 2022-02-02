#!/usr/bin/env python3

# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for the HTML writer.
"""

import os
from pathlib import Path
import unittest

import docutils
import docutils.core


class TestHTML4Template(unittest.TestCase, docutils.SettingsSpec):

    """
    Test case for publish.
    """

    settings_default_overrides = {"_disable_config": True,
                                  "strict_visitor": True}

    def test_html4_css1_template(self):
        output = docutils.core.publish_string(
            source=case_input,
            reader_name="standalone",
            parser_name="restructuredtext",
            writer_name="html4",
            settings_spec=self,
            settings_overrides={
                'template': os.path.abspath(os.path.join(__file__, "..", "..",
                                                         'data', 'full-template.txt')),
                'stylesheet_path': '/test.css',
                'embed_stylesheet': False,
            })
        self.assertEqual(output, case_expected)


drive_prefix = Path.cwd().drive

case_input = """\
================
 Document Title
================
----------
 Subtitle
----------

:Author: Me

.. footer:: footer text

Section
=======

Some text.
"""

case_expected = fr'''head_prefix = """\
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>"""


head = """\
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="generator" content="Docutils {docutils.__version__}: https://docutils.sourceforge.io/" />
<title>Document Title</title>
<meta name="author" content="Me" />"""


stylesheet = """\
<link rel="stylesheet" href="{drive_prefix}/test.css" type="text/css" />"""


body_prefix = """\
</head>
<body>
<div class="document" id="document-title">"""


body_pre_docinfo = """\
<h1 class="title">Document Title</h1>
<h2 class="subtitle" id="subtitle">Subtitle</h2>"""


docinfo = """\
<table class="docinfo" frame="void" rules="none">
<col class="docinfo-name" />
<col class="docinfo-content" />
<tbody valign="top">
<tr><th class="docinfo-name">Author:</th>
<td>Me</td></tr>
</tbody>
</table>"""


body = """\
<div class="section" id="section">
<h1>Section</h1>
<p>Some text.</p>
</div>"""


body_suffix = """\
</div>
<div class="footer">
<hr class="footer" />
footer text
</div>
</body>
</html>"""


head_prefix = """\
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>"""


head = """\
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="generator" content="Docutils {docutils.__version__}: https://docutils.sourceforge.io/" />
<title>Document Title</title>
<meta name="author" content="Me" />"""


stylesheet = """\
<link rel="stylesheet" href="{drive_prefix}/test.css" type="text/css" />"""


body_prefix = """\
</head>
<body>
<div class="document" id="document-title">"""


body_pre_docinfo = """\
<h1 class="title">Document Title</h1>
<h2 class="subtitle" id="subtitle">Subtitle</h2>"""


docinfo = """\
<table class="docinfo" frame="void" rules="none">
<col class="docinfo-name" />
<col class="docinfo-content" />
<tbody valign="top">
<tr><th class="docinfo-name">Author:</th>
<td>Me</td></tr>
</tbody>
</table>"""


body = """\
<div class="section" id="section">
<h1>Section</h1>
<p>Some text.</p>
</div>"""


body_suffix = """\
</div>
<div class="footer">
<hr class="footer" />
footer text
</div>
</body>
</html>"""


title = """\
Document Title"""


subtitle = """\
Subtitle"""


header = """\
"""


footer = """\
<div class="footer">
<hr class="footer" />
footer text
</div>"""


meta = """\
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="generator" content="Docutils {docutils.__version__}: https://docutils.sourceforge.io/" />
<meta name="author" content="Me" />"""


fragment = """\
<div class="section" id="section">
<h1>Section</h1>
<p>Some text.</p>
</div>"""


html_prolog = """\
<?xml version="1.0" encoding="%s" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">"""


html_head = """\
<meta http-equiv="Content-Type" content="text/html; charset=%s" />
<meta name="generator" content="Docutils {docutils.__version__}: https://docutils.sourceforge.io/" />
<title>Document Title</title>
<meta name="author" content="Me" />"""


html_title = """\
<h1 class="title">Document Title</h1>"""


html_subtitle = """\
<h2 class="subtitle" id="subtitle">Subtitle</h2>"""


html_body = """\
<div class="document" id="document-title">
<h1 class="title">Document Title</h1>
<h2 class="subtitle" id="subtitle">Subtitle</h2>
<table class="docinfo" frame="void" rules="none">
<col class="docinfo-name" />
<col class="docinfo-content" />
<tbody valign="top">
<tr><th class="docinfo-name">Author:</th>
<td>Me</td></tr>
</tbody>
</table>
<div class="section" id="section">
<h1>Section</h1>
<p>Some text.</p>
</div>
</div>
<div class="footer">
<hr class="footer" />
footer text
</div>"""
'''

if __name__ == '__main__':
    unittest.main()
