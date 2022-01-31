#! /usr/bin/env python3

# $Id$
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test module for the --record-dependencies option.
"""

import os.path
import unittest

import docutils.core
import docutils.io
from docutils.parsers.rst.directives.images import PIL
import docutils.utils


class DevNull:
    """Output sink."""
    def write(self, string): pass
    def close(self): pass


# docutils.utils.DependencyList records POSIX paths,
# i.e. "/" as a path separator even on Windows (not os.path.join).
paths = {'include': 'data/include.txt',  # included rst file
         'raw': 'data/raw.txt',      # included raw "HTML file"
         'scaled-image': '../docs/user/rst/images/biohazard.png',
         'figure-image': '../docs/user/rst/images/title.png',
         'stylesheet': 'data/stylesheet.txt',
         }

# avoid latex writer future warnings:
latex_settings_overwrites = {'legacy_column_widths': False,
                             'use_latex_citations': True}


def get_record(**settings):
    record_file = 'record.txt'
    recorder = docutils.utils.DependencyList(record_file)
    # (Re) create the record file by running a conversion:
    settings.setdefault('source_path',
                        os.path.join('data', 'dependencies.txt'))
    settings.setdefault('settings_overrides', {})
    settings['settings_overrides'].update(_disable_config=True,
                                          record_dependencies=recorder)
    docutils.core.publish_file(destination=DevNull(), **settings)
    recorder.close()
    # Read the record file:
    record = docutils.io.FileInput(source_path=record_file, encoding='utf8')
    return record.read().splitlines()


class RecordDependenciesTests(unittest.TestCase):
    def test_dependencies_xml(self):
        # Note: currently, raw input files are read (and hence recorded) while
        # parsing even if not used in the chosen output format.
        # This should change (see parsers/rst/directives/misc.py).
        keys = ['include', 'raw']
        if PIL:
            keys += ['figure-image']
        expected = sorted(paths[key] for key in keys)
        record = sorted(get_record(writer_name='xml'))
        self.assertEqual(record, expected)

    def test_dependencies_html(self):
        keys = ['include', 'raw']
        if PIL:
            keys += ['figure-image', 'scaled-image']
        expected = sorted(paths[key] for key in keys)
        # stylesheets are tested separately in test_stylesheet_dependencies():
        so = {'stylesheet_path': None, 'stylesheet': None}
        record = sorted(get_record(writer_name='html',
                                        settings_overrides=so))
        self.assertEqual(record, expected)

    def test_dependencies_latex(self):
        # since 0.9, the latex writer records only really accessed files, too.
        # Note: currently, raw input files are read (and hence recorded) while
        # parsing even if not used in the chosen output format.
        # This should change (see parsers/rst/directives/misc.py).
        keys = ['include', 'raw']
        if PIL:
            keys += ['figure-image']
        expected = sorted(paths[key] for key in keys)
        record = sorted(get_record(writer_name='latex',
                                   settings_overrides=latex_settings_overwrites))
        self.assertEqual(record, expected)

    def test_csv_dependencies(self):
        csvsource = os.path.join('data', 'csv_dep.txt')
        self.assertEqual(get_record(source_path=csvsource),
                         ['data/csv_data.txt'])

    def test_stylesheet_dependencies(self):
        stylesheet = paths['stylesheet']
        so = {'stylesheet_path': paths['stylesheet'],
              'stylesheet': None}
        so.update(latex_settings_overwrites)
        so['embed_stylesheet'] = False
        record = get_record(writer_name='html', settings_overrides=so)
        self.assertTrue(stylesheet not in record,
                        f'{stylesheet!r} should not be in {record!r}')
        record = get_record(writer_name='latex', settings_overrides=so)
        self.assertTrue(stylesheet not in record,
                        f'{stylesheet!r} should not be in {record!r}')

        so['embed_stylesheet'] = True
        record = get_record(writer_name='html', settings_overrides=so)
        self.assertTrue(stylesheet in record,
                        f'{stylesheet!r} should be in {record!r}')
        so['embed_stylesheet'] = True
        record = get_record(writer_name='latex', settings_overrides=so)
        self.assertTrue(stylesheet in record,
                        f'{stylesheet!r} should be in {record!r}')

    def tearDown(self) -> None:
        os.unlink("record.txt")


if __name__ == '__main__':
    unittest.main()
