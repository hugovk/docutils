#!/usr/bin/env python3

# $Id$
# Authors: Engelbert Gruber <grubert@users.sourceforge.net>;
#          David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Tests for language module completeness.

Specify a language code (e.g. "de") as a command-line parameter to test only
that language.
"""

import os
import re

import unittest

import docutils.frontend
import docutils.languages
from docutils.parsers.rst import directives
from docutils.parsers.rst import roles
import docutils.parsers.rst.languages
import docutils.utils

_settings = docutils.frontend.get_default_settings()
_reporter = docutils.utils.new_reporter('', _settings)

REFERENCE_LANGUAGE = 'en'
REF = docutils.languages.get_language(REFERENCE_LANGUAGE, _reporter)

LANGUAGE_MODULE_PATTERN = re.compile(r'^([a-z]{2,3}(_[a-z]{2,8})*)\.py$')


def get_languages():
    """
    Get installed language translations from docutils.languages and from
    docutils.parsers.rst.languages.
    """
    translations = set()
    for mod in (os.listdir(docutils.languages.__path__[0])
                + os.listdir(docutils.parsers.rst.languages.__path__[0])):
        match = LANGUAGE_MODULE_PATTERN.match(mod)
        if match:
            translations.add(match.group(1))
    return [
        *translations,
        # test language tag normalization:
        'en_gb', 'en_US', 'en-CA', 'de-DE', 'de-AT-1901', 'pt-BR', 'pt-foo-BR',
        # test that locally created language files are also loaded.
        # requires local_dummy_lang.py in test directory (testroot)
        # The local_dummy_lang.py contains all the fields from both
        # the docutils language tags and the parser.rst language tags
        'local_dummy_lang',
    ]


def _xor(ref_dict, l_dict):
    """
    Returns entries that are only in one dictionary.
    (missing_in_lang, more_than_in_ref).
    """
    missing  = []   # in ref but not in l.
    too_much = []   # in l but not in ref.
    for label in ref_dict.keys():
        if label not in l_dict:
            missing.append(label)
    for label in l_dict.keys():
        if label not in ref_dict:
            too_much.append(label)
    return missing, too_much


def _invert(adict):
    """Return an inverted (keys & values swapped) dictionary."""
    inverted = {}
    for key, value in adict.items():
        inverted[value] = key
    return inverted


class TestLanguages(unittest.TestCase):
    def test_labels(self):
        for language in get_languages():
            with self.subTest(id=f"{language}.py"):
                try:
                    module = docutils.languages.get_language(language, _reporter)
                    if not module:
                        raise ImportError
                except ImportError:
                    self.fail(f'No docutils.languages.{language} module.')
                missed, unknown = _xor(REF.labels, module.labels)
                if missed or unknown:
                    self.fail(
                        f'Module docutils.languages.{language}.labels:\n'
                        f'    Missed: {str(missed)}; Unknown: {str(unknown)}')

    def test_bibliographic_fields(self):
        for language in get_languages():
            with self.subTest(id=f"{language}.py"):
                try:
                    module = docutils.languages.get_language(language, _reporter)
                    if not module:
                        raise ImportError
                except ImportError:
                    self.fail(f'No docutils.languages.{language} module.')
                missed, unknown = _xor(
                    _invert(REF.bibliographic_fields),
                    _invert(module.bibliographic_fields))
                if missed or unknown:
                    self.fail(
                        f'Module docutils.languages.{language}.bibliographic_fields:\n'
                        f'    Missed: {missed}; Unknown: {unknown}')

    def test_directives(self):
        for language in get_languages():
            with self.subTest(id=f"{language}.py"):
                try:
                    module = docutils.parsers.rst.languages.get_language(
                        language)
                    if not module:
                        raise ImportError
                except ImportError:
                    self.fail(f'No docutils.parsers.rst.languages.{language} module.')
                failures = []
                for d in module.directives.keys():
                    try:
                        func, msg = directives.directive(d, module, None)
                        if not func:
                            failures.append(f'"{d}": unknown directive')
                    except Exception as error:
                        failures.append(f'"{d}": {error}')
                inverted = _invert(module.directives)
                canonical = sorted(directives._directive_registry.keys())
                canonical.remove('restructuredtext-test-directive')
                for name in canonical:
                    if name not in inverted:
                        failures.append('"%s": translation missing' % name)
                if failures:
                    text = (f'Module docutils.parsers.rst.languages.{language}:\n'
                            + '\n    '.join(failures))
                    self.fail(text.encode('raw_unicode_escape'))

    def test_roles(self):
        for language in get_languages():
            with self.subTest(id=f"{language}.py"):
                module = docutils.parsers.rst.languages.get_language(
                    language)
                if not module:
                    self.fail(f'No docutils.parsers.rst.languages.{language} module.')
                if not hasattr(module, "roles"):
                    self.fail('No "roles" mapping in docutils.parsers.rst.languages.'
                              f'{language} module.')
                failures = []
                for d in module.roles.values():
                    try:
                        roles._role_registry[d]
                    except KeyError as error:
                        failures.append(f'"{d}": {error}')
                inverted = _invert(module.roles)
                canonical = sorted(roles._role_registry.keys())
                canonical.remove('restructuredtext-unimplemented-role')
                for name in canonical:
                    if name not in inverted:
                        failures.append(f'"{name}": translation missing')
                if failures:
                    text = (f'Module docutils.parsers.rst.languages.{language}:\n'
                            + '\n    '.join(failures))
                    self.fail(text.encode('raw_unicode_escape'))


if __name__ == '__main__':
    unittest.main()
