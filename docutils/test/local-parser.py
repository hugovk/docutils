# $Id$
# Authors: Engelbert Gruber <grubert@users.sourceforge.net>
#          Toshio Kuratomi <toshio@fedoraproject.org>
# Copyright: This module is put into the public domain.

"""
mini-parser to test get_parser_class with local parser
"""

from docutils import parsers


class Parser(parsers.Parser):

    supported = ('dummy',)
    """Formats this reader supports."""

    def parser(self, inputstring, document):
        self.setup_parse(inputstring, document)
        self.finish_parse()
