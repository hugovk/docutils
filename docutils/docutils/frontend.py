# $Id$
# Author: David Goodger <goodger@python.org>
# Copyright: This module has been placed in the public domain.

"""
Command-line and common processing for Docutils front-end tools.

This module is provisional.

Applications should use the high-level API provided by `docutils.core`.
See https://docutils.sourceforge.io/docs/api/runtime-settings.html.

Exports the following classes:

* `OptionParser`: Standard Docutils command-line processing.
* `Option`: Customized version of `optparse.Option`; validation support.
* `Values`: Runtime settings; objects are simple structs
  (``object.attribute``).  Supports cumulative list settings (attributes).
* `ConfigParser`: Standard Docutils config file processing.

Also exports the following functions:

* Option callbacks: `store_multiple()`, `read_config_file()`.
* Setting validators: `validate_encoding()`,
  `validate_encoding_error_handler()`,
  `validate_encoding_and_error_handler()`,
  `validate_boolean()`, `validate_ternary()`, `validate_threshold()`,
  `validate_colon_separated_string_list()`,
  `validate_comma_separated_list()`,
  `validate_dependency_file()`.
* `make_paths_absolute()`.
* SettingSpec creation: `filter_settings_spec()`.
"""

__docformat__ = 'reStructuredText'

import argparse
import codecs
import configparser
import os
import os.path
import sys
import warnings

import docutils
import docutils.io
import docutils.nodes
import docutils.utils


def __getattr__(name):
    if name in {"SUPPRESS_HELP", "store_multiple", "read_config_file",
                "make_paths_absolute", "make_one_path_absolute", "Values",
                "Option", "OptionParser", "ConfigParser"}:
        warnings.warn(f"'{name}' is deprecated, and will be removed in "
                      f"Docutils 1.2.", DeprecationWarning, stacklevel=2)
    try:
        return globals()[name]
    except KeyError:
        raise AttributeError(f"module {__name__} has no attribute {name}")


SUPPRESS_HELP = None

# Lookup table for boolean configuration file settings
_BOOLEANS = {"1": True,  "on":  True,  "yes": True,  "true":  True,
             "0": False, "off": False, "no":  False, "false": False, "": False}

# Lookup table for --report and --halt threshold values
_THRESHOLDS = {"info": 1, "warning": 2, "error": 3, "severe": 4, "none": 5}


class _LegacyCallbackAction(argparse.Action):
    _legacy_callable = lambda option, opt, value, parser, *args, **kwargs: ...
    _callback_args = ()

    def __call__(self, parser, namespace, values, option_string=None):
        self._legacy_callable(
            self.dest, None, values, parser, *self._callback_args
        )


def store_multiple(option, opt, value, parser, *args, **kwargs):
    """
    Store multiple values in `parser.values`.  (Option callback.)

    Store `None` for each attribute named in `args`, and store the value for
    each key (attribute name) in `kwargs`.
    """
    for attribute in args:
        setattr(parser.values, attribute, None)
    for key, value in kwargs.items():
        setattr(parser.values, key, value)


class read_config_file(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        """
        Read a configuration file during option processing.
        """
        try:
            config_parser = ConfigParser()
            config_parser.read(values, OptionParser())
            new_settings = {s: dict(config_parser.items(s)) for s in config_parser.sections()}
        except ValueError as err:
            parser.error(str(err))
        else:
            parser.set_defaults(**new_settings)


def validate_encoding(value):
    try:
        codecs.lookup(value)
    except LookupError:
        raise LookupError(f'unknown encoding: "{value}"')
    return value


# Can't be a simple validator as it has side effects :(
# This is special-cased in the settings-spec parsing code
class validate_encoding_and_error_handler(argparse.Action):
    def __call__(self, parser, namespace, value, option_string=None):
        """
        Side-effect: if an error handler is included in the value, it is inserted
        into the appropriate place as if it was a separate setting/option.
        """
        if ':' in value:
            encoding, handler = value.split(':', 1)
            validate_encoding_error_handler(handler)
            setattr(namespace, self.dest + '_error_handler', handler)
        else:
            encoding = value
        validate_encoding(encoding)
        setattr(namespace, self.dest, encoding)


# terrible hack -- the above action class is replaced with this function when
# parsing from a config file.
def _validate_encoding_and_error_handler_config_parser(
        value, argument, config_section, config_parser
):
    """
    Side-effect: if an error handler is included in the value, it is inserted
    into the appropriate place as if it was a separate setting/option.
    """
    if ':' in value:
        encoding, handler = value.split(':', 1)
        validate_encoding_error_handler(handler)
        config_parser.set(config_section, argument + '_error_handler', handler)
    else:
        encoding = value
    validate_encoding(encoding)
    return encoding

# Simple validators
# ########################################

def validate_encoding_error_handler(value):
    try:
        codecs.lookup_error(value)
    except LookupError:
        raise LookupError(
            f'unknown encoding error handler: "{value}" (choices: '
            '"strict", "ignore", "replace", "backslashreplace", '
            '"xmlcharrefreplace", and possibly others; see documentation for '
            'the Python ``codecs`` module)')
    return value


def validate_boolean(value):
    """Check/normalize boolean settings:
         True:  '1', 'on', 'yes', 'true'
         False: '0', 'off', 'no','false', ''
    """
    if isinstance(value, bool):
        return value
    try:
        return _BOOLEANS[value.strip().lower()]
    except KeyError:
        raise LookupError('unknown boolean value: "%s"' % value)


def validate_ternary(value):
    """Check/normalize three-value settings:
         True:  '1', 'on', 'yes', 'true'
         False: '0', 'off', 'no','false', ''
         any other value: returned as-is.
    """
    if isinstance(value, (bool, type(None))):
        return value
    try:
        return _BOOLEANS[value.strip().lower()]
    except KeyError:
        return value


def validate_nonnegative_int(value):
    value = int(value)
    if value < 0:
        raise ValueError('negative value; must be positive or zero')
    return value


def validate_threshold(value):
    try:
        return int(value)
    except ValueError:
        try:
            return _THRESHOLDS[value.lower()]
        except (KeyError, AttributeError):
            raise LookupError(f'unknown threshold: {value!r}.')


def validate_colon_separated_string_list(value):
    if isinstance(value, list):
        last = value.pop()
        value.extend(last.split(":"))
        return value
    return value.split(":")


def validate_comma_separated_list(value):
    """Check/normalize list arguments (split at "," and strip whitespace).
    """
    # `value` may be ``bytes``, ``str``, or a ``list`` (when  given as
    # command line option and "action" is "append").
    if not isinstance(value, list):
        value = [value]
    # this function is called for every option added to `value`
    # -> split the last item and append the result:
    last = value.pop()
    for i in last.split(","):
        strip = i.strip(" \t\n")
        if strip:
            value.append(strip)
    return value


def validate_url_trailing_slash(value):
    if not value:
        return "./"
    if value.endswith("/"):
        return value
    return value + "/"


def validate_dependency_file(value):
    try:
        return docutils.utils.DependencyList(value)
    except OSError:
        # TODO: warn/info?
        return docutils.utils.DependencyList(None)


def validate_strip_class(value):
    # value is a comma separated string list:
    value = validate_comma_separated_list(value)
    # validate list elements:
    for cls in value:
        normalised = docutils.nodes.make_id(cls)
        if cls != normalised:
            raise ValueError(
                f"Invalid class value {cls!r} (perhaps {normalised!r}?)"
            )
    return value


def validate_smartquotes_locales(value):
    """Check/normalize a comma separated list of smart quote definitions.

    Return a list of (language-tag, quotes) string tuples."""

    # value is a comma separated string list:
    value = validate_comma_separated_list(value)
    # validate list elements
    lc_quotes = []
    for item in value:
        try:
            lang, quotes = item.split(':', 1)
        except AttributeError:
            # this function is called for every option added to `value`
            # -> ignore if already a tuple:
            lc_quotes.append(item)
            continue
        except ValueError:
            raise ValueError(
                f'Invalid value "{item.encode("ascii", "backslashreplace")}". '
                'Format is "<language>:<quotes>".'
            )
        # parse colon separated string list:
        quotes = quotes.strip()
        multichar_quotes = quotes.split(':')
        if len(multichar_quotes) == 4:
            quotes = multichar_quotes
        elif len(quotes) != 4:
            raise ValueError(
                f'Invalid value "{item.encode("ascii", "backslashreplace")}". '
                'Please specify 4 quotes\n'
                             '    (primary open/close; secondary open/close).'
            )
        lc_quotes.append((lang, quotes))
    return lc_quotes


def make_paths_absolute(pathdict, keys, base_path=None):
    """
    Interpret filesystem path settings relative to the `base_path` given.

    Paths are values in `pathdict` whose keys are in `keys`.  Get `keys` from
    `OptionParser.relative_path_settings`.
    """
    if base_path is None:
        base_path = os.getcwd()
    for key in keys:
        if key in pathdict:
            value = pathdict[key]
            if isinstance(value, list):
                value = [make_one_path_absolute(base_path, path)
                         for path in value]
            elif value:
                value = make_one_path_absolute(base_path, value)
            pathdict[key] = value


def make_one_path_absolute(base_path, path):
    return os.path.abspath(os.path.join(base_path, path))


def filter_settings_spec(settings_spec, *exclude, **replace):
    """Return a copy of `settings_spec` excluding/replacing some settings.

    `settings_spec` is a tuple of configuration settings
    (cf. `docutils.SettingsSpec.settings_spec`).

    Optional positional arguments are names of to-be-excluded settings.
    Keyword arguments are option specification replacements.
    (See the html4strict writer for an example.)
    """
    settings = [*settings_spec]
    # every third item is a sequence of option tuples
    for i in range(2, len(settings), 3):
        newopts = []
        for opt_spec in settings[i]:
            # opt_spec is ("<help>", [<option strings>], {<keyword args>})
            opt_name = next(opt_string[2:].replace('-', '_')
                            for opt_string in opt_spec[1]
                            if opt_string.startswith('--'))
            if opt_name in exclude:
                continue
            if opt_name in replace.keys():
                newopts.append(replace[opt_name])
            else:
                newopts.append(opt_spec)
        settings[i] = tuple(newopts)
    return tuple(settings)


class Values:
    """
    Simple class to store values for attribute access.
    """

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            self.__dict__[name] = value

        # Set up a dependency list in case it is needed.
        if self.__dict__.get("record_dependencies") is None:
            self.record_dependencies = docutils.utils.DependencyList()

    def __eq__(self, other):
        if not isinstance(other, Values):
            return NotImplemented
        return self.__dict__ == other.__dict__

    def __contains__(self, key):
        return key in self.__dict__

    def __repr__(self):
        args_pairs = []
        non_str = {}
        for name, value in self.__dict__.items():
            if name.isidentifier():
                args_pairs.append(f"{name}={repr(value)}")
            else:
                non_str[name] = value
        if non_str:
            args_pairs.append(f"**{repr(non_str)}")
        return "{}({})".format(self.__class__.__name__, ", ".join(args_pairs))

    def copy(self):
        """Return a shallow copy of self."""
        return self.__class__(**self.__dict__)

    def setdefault(self, name, default):
        return self.__dict__.setdefault(name, default)

    def update(self, other):
        self.__dict__.update(other.__dict__)


class Option: ...


class _SettingsSpec(docutils.SettingsSpec):

    """
    Parser for command-line and library use.  The `settings_spec`
    specification here and in other Docutils components are merged to build
    the set of command-line options and runtime settings for this process.

    Common settings (defined below) and component-specific settings must not
    conflict.  Short options are reserved for common settings, and components
    are restricted to using long options.
    """

    standard_config_files = [
        '/etc/docutils.conf',               # system-wide
        './docutils.conf',                  # project-specific
        os.path.expanduser('~/.docutils')]  # user-specific
    """Docutils configuration files, using ConfigParser syntax.  Later files
    override earlier ones."""

    threshold_choices = 'info 1 warning 2 error 3 severe 4 none 5'.split()
    """Possible inputs for for --report and --halt threshold values."""

    thresholds = {**_THRESHOLDS}
    """Lookup table for --report and --halt threshold values."""

    booleans = {**_BOOLEANS}
    """Lookup table for boolean configuration file settings."""

    default_error_encoding = (getattr(sys.stderr, 'encoding', None)
                              or docutils.io.locale_encoding or 'ascii')

    default_error_encoding_error_handler = 'backslashreplace'

    settings_spec = (
        'General Docutils Options',
        None,
        (('Specify the document title as metadata.',
          ['--title'], {}),
         ('Include a "Generated by Docutils" credit and link.',
          ['--generator', '-g'], {'action': 'store_true',
                                  'validator': validate_boolean}),
         ('Do not include a generator credit.',
          ['--no-generator'], {'action': 'store_false', 'dest': 'generator'}),
         ('Include the date at the end of the document (UTC).',
          ['--date', '-d'], {'action': 'store_const', 'const': '%Y-%m-%d',
                             'dest': 'datestamp'}),
         ('Include the time & date (UTC).',
          ['--time', '-t'], {'action': 'store_const',
                             'const': '%Y-%m-%d %H:%M UTC',
                             'dest': 'datestamp'}),
         ('Do not include a datestamp of any kind.',
          ['--no-datestamp'], {'action': 'store_const', 'const': None,
                               'dest': 'datestamp'}),
         ('Include a "View document source" link.',
          ['--source-link', '-s'], {'action': 'store_true',
                                    'validator': validate_boolean}),
         ('Use <URL> for a source link; implies --source-link.',
          ['--source-url'], {'metavar': '<URL>'}),
         ('Do not include a "View document source" link.',
          ['--no-source-link'],
          {'action': 'callback', 'callback': store_multiple,
           'callback_args': ('source_link', 'source_url')}),
         ('Link from section headers to TOC entries.  (default)',
          ['--toc-entry-backlinks'],
          {'dest': 'toc_backlinks', 'action': 'store_const', 'const': 'entry',
           'default': 'entry'}),
         ('Link from section headers to the top of the TOC.',
          ['--toc-top-backlinks'],
          {'dest': 'toc_backlinks', 'action': 'store_const', 'const': 'top'}),
         ('Disable backlinks to the table of contents.',
          ['--no-toc-backlinks'],
          {'dest': 'toc_backlinks', 'action': 'store_false'}),
         ('Link from footnotes/citations to references. (default)',
          ['--footnote-backlinks'],
          {'action': 'store_true', 'default': 1,
           'validator': validate_boolean}),
         ('Disable backlinks from footnotes and citations.',
          ['--no-footnote-backlinks'],
          {'dest': 'footnote_backlinks', 'action': 'store_false'}),
         ('Enable section numbering by Docutils.  (default)',
          ['--section-numbering'],
          {'action': 'store_true', 'dest': 'sectnum_xform',
           'default': 1, 'validator': validate_boolean}),
         ('Disable section numbering by Docutils.',
          ['--no-section-numbering'],
          {'action': 'store_false', 'dest': 'sectnum_xform'}),
         ('Remove comment elements from the document tree.',
          ['--strip-comments'],
          {'action': 'store_true', 'validator': validate_boolean}),
         ('Leave comment elements in the document tree. (default)',
          ['--leave-comments'],
          {'action': 'store_false', 'dest': 'strip_comments'}),
         ('Remove all elements with classes="<class>" from the document tree. '
          'Warning: potentially dangerous; use with caution. '
          '(Multiple-use option.)',
          ['--strip-elements-with-class'],
          {'action': 'append', 'dest': 'strip_elements_with_classes',
           'metavar': '<class>', 'validator': validate_strip_class}),
         ('Remove all classes="<class>" attributes from elements in the '
          'document tree. Warning: potentially dangerous; use with caution. '
          '(Multiple-use option.)',
          ['--strip-class'],
          {'action': 'append', 'dest': 'strip_classes',
           'metavar': '<class>', 'validator': validate_strip_class}),
         ('Report system messages at or higher than <level>: "info" or "1", '
          '"warning"/"2" (default), "error"/"3", "severe"/"4", "none"/"5"',
          ['--report', '-r'], {'choices': threshold_choices, 'default': 2,
                               'dest': 'report_level', 'metavar': '<level>',
                               'validator': validate_threshold}),
         ('Report all system messages.  (Same as "--report=1".)',
          ['--verbose', '-v'], {'action': 'store_const', 'const': 1,
                                'dest': 'report_level'}),
         ('Report no system messages.  (Same as "--report=5".)',
          ['--quiet', '-q'], {'action': 'store_const', 'const': 5,
                              'dest': 'report_level'}),
         ('Halt execution at system messages at or above <level>.  '
          'Levels as in --report.  Default: 4 (severe).',
          ['--halt'], {'choices': threshold_choices, 'dest': 'halt_level',
                       'default': 4, 'metavar': '<level>',
                       'validator': validate_threshold}),
         ('Halt at the slightest problem.  Same as "--halt=info".',
          ['--strict'], {'action': 'store_const', 'const': 1,
                         'dest': 'halt_level'}),
         ('Enable a non-zero exit status for non-halting system messages at '
          'or above <level>.  Default: 5 (disabled).',
          ['--exit-status'], {'choices': threshold_choices,
                              'dest': 'exit_status_level',
                              'default': 5, 'metavar': '<level>',
                              'validator': validate_threshold}),
         ('Enable debug-level system messages and diagnostics.',
          ['--debug'], {'action': 'store_true', 'validator': validate_boolean}),
         ('Disable debug output.  (default)',
          ['--no-debug'], {'action': 'store_false', 'dest': 'debug'}),
         ('Send the output of system messages to <file>.',
          ['--warnings'], {'dest': 'warning_stream', 'metavar': '<file>'}),
         ('Enable Python tracebacks when Docutils is halted.',
          ['--traceback'], {'action': 'store_true', 'default': None,
                            'validator': validate_boolean}),
         ('Disable Python tracebacks.  (default)',
          ['--no-traceback'], {'dest': 'traceback', 'action': 'store_false'}),
         ('Specify the encoding and optionally the '
          'error handler of input text.  Default: <locale-dependent>:strict.',
          ['--input-encoding', '-i'],
          {'metavar': '<name[:handler]>',
           'validator': validate_encoding_and_error_handler}),
         ('Specify the error handler for undecodable characters.  '
          'Choices: "strict" (default), "ignore", and "replace".',
          ['--input-encoding-error-handler'],
          {'default': 'strict', 'validator': validate_encoding_error_handler}),
         ('Specify the text encoding and optionally the error handler for '
          'output.  Default: UTF-8:strict.',
          ['--output-encoding', '-o'],
          {'metavar': '<name[:handler]>', 'default': 'utf-8',
           'validator': validate_encoding_and_error_handler}),
         ('Specify error handler for unencodable output characters; '
          '"strict" (default), "ignore", "replace", '
          '"xmlcharrefreplace", "backslashreplace".',
          ['--output-encoding-error-handler'],
          {'default': 'strict', 'validator': validate_encoding_error_handler}),
         ('Specify text encoding and error handler for error output.  '
          'Default: %s:%s.'
          % (default_error_encoding, default_error_encoding_error_handler),
          ['--error-encoding', '-e'],
          {'metavar': '<name[:handler]>', 'default': default_error_encoding,
           'validator': validate_encoding_and_error_handler}),
         ('Specify the error handler for unencodable characters in '
          'error output.  Default: %s.'
          % default_error_encoding_error_handler,
          ['--error-encoding-error-handler'],
          {'default': default_error_encoding_error_handler,
           'validator': validate_encoding_error_handler}),
         ('Specify the language (as BCP 47 language tag).  Default: en.',
          ['--language', '-l'], {'dest': 'language_code', 'default': 'en',
                                 'metavar': '<name>'}),
         ('Write output file dependencies to <file>.',
          ['--record-dependencies'],
          {'metavar': '<file>', 'validator': validate_dependency_file,
           'default': None}),           # default set in Values class
         ('Read configuration settings from <file>, if it exists.',
          ['--config'], {'metavar': '<file>', 'type': 'string',
                         'action': 'callback', 'callback': read_config_file}),
         ("Show this program's version number and exit.",
          ['--version', '-V'], {'action': 'version'}),
         ('Show this help message and exit.',
          ['--help', '-h'], {'action': 'help'}),
         # Typically not useful for non-programmatical use:
         (SUPPRESS_HELP, ['--id-prefix'], {'default': ''}),
         (SUPPRESS_HELP, ['--auto-id-prefix'], {'default': '%'}),
         # Hidden options, for development use only:
         (SUPPRESS_HELP, ['--dump-settings'], {'action': 'store_true'}),
         (SUPPRESS_HELP, ['--dump-internals'], {'action': 'store_true'}),
         (SUPPRESS_HELP, ['--dump-transforms'], {'action': 'store_true'}),
         (SUPPRESS_HELP, ['--dump-pseudo-xml'], {'action': 'store_true'}),
         (SUPPRESS_HELP, ['--expose-internal-attribute'],
          {'action': 'append', 'dest': 'expose_internals',
           'validator': validate_colon_separated_string_list}),
         (SUPPRESS_HELP, ['--strict-visitor'], {'action': 'store_true'}),
         ))
    """Runtime settings and command-line options common to all Docutils front
    ends.  Setting specs specific to individual Docutils components are also
    used (see `populate_from_components()`)."""

    settings_defaults = {'_disable_config': None,
                         '_source': None,
                         '_destination': None,
                         '_config_files': None}
    """Defaults for settings that don't have command-line option equivalents."""

    relative_path_settings = ('warning_stream',)

    config_section = 'general'

    version_template = f'%(prog) (Docutils {docutils.__version__} [{docutils.__version_details__}], Python {sys.version.split()[0]}, on {sys.platform})'
    """Default version message."""


class _ArgumentParser(argparse.ArgumentParser):
    relative_path_settings = ()  # set in _SettingsSpec

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.arg_defaults = {}
        """Mapping of argument name to argument default value."""

        self.config_files = []
        """List of paths of applied configuration files."""

    def set_defaults(self, **kwargs):
        argparse.ArgumentParser.set_defaults(self, **kwargs)
        self.arg_defaults.update(kwargs)

    def parse_args(self, args=None, namespace=None):
        args = super().parse_args(args, namespace)
        if args._source and args._source == args._destination:
            self.error('Do not specify the same file for both source and '
                       'destination.  It will clobber the source file.')
        make_paths_absolute(args.__dict__, self.relative_path_settings)
        args._config_files = self.config_files
        return Values(**args.__dict__)


class OptionParser(_ArgumentParser, _SettingsSpec):
    def __init__(self, components=(), defaults=None, read_config_files=None,
                 *args, **kwargs):
        """
        `components` is a list of Docutils components each containing a
        ``.settings_spec`` attribute.  `defaults` is a mapping of setting
        default overrides.
        """

        self._list_args = set()
        """Set of list-type settings."""

        super().__init__(
            add_help=False,
            formatter_class=argparse.HelpFormatter,
            *args,
            **kwargs
        )

        # Make an instance copy (it will be modified):
        self.relative_path_settings = [*self.relative_path_settings]

        self.components = (self, *components)
        self.populate_from_components(self.components)

        if self.get_default("version") is None:
            self.add_argument('--version', action='version',
                              version=self.version_template)

        if defaults:
            self.set_defaults(**defaults)

        if read_config_files and not self.get_default("_disable_config"):
            try:
                settings = {}
                for file in self.get_standard_config_files():
                    if not os.path.isfile(file):
                        continue
                    new = get_config_file_settings(
                        self,
                        file,
                        self.config_files,
                        self.components,
                        self._list_args,
                        self.relative_path_settings
                    )
                    settings = _merge_with_list_args(
                        settings, new, self._list_args)
                self.set_defaults(**settings)
            except ValueError as err:
                self.error(str(err))

        def _stdio_validator(value):
            return None if value == "-" else value  # "-" means stdin/stdout

        self.add_argument("_source", nargs="?", metavar="SOURCE",
                          type=_stdio_validator)
        self.add_argument("_destination", nargs="?", metavar="DESTINATION",
                          type=_stdio_validator)

    def populate_from_components(self, components):
        """
        For each component, first populate from the `SettingsSpec.settings_spec`
        structure, then from the `SettingsSpec.settings_defaults` dictionary.
        After all components have been processed, check for and populate from
        each component's `SettingsSpec.settings_default_overrides` dictionary.
        """
        overrides_list = []
        for component in components:
            if component is None:
                continue
            spec = component.settings_spec
            chunked = zip(spec[::3], spec[1::3], spec[2::3])
            for (title, description, option_spec) in chunked:
                if title:
                    group = self.add_argument_group(title, description)
                else:
                    group = self  # single options
                for (help_text, option_strings, kwargs) in option_spec:
                    _create_option(
                        group,
                        help_text, option_strings, kwargs.copy(),
                        self.arg_defaults,
                        self._list_args
                    )

            # Update defaults from component
            if component.settings_defaults:
                self.set_defaults(**component.settings_defaults)

            # Append paths
            self.relative_path_settings += component.relative_path_settings

            # Save settings_default_overrides
            if component.settings_default_overrides:
                overrides_list.append(component.settings_default_overrides)
        # Apply settings_default_overrides in order
        for default_overrides in overrides_list:
            self.set_defaults(**default_overrides)

    @classmethod
    def get_standard_config_files(cls):
        """Return list of config files, from environment or standard."""
        if 'DOCUTILSCONFIG' not in os.environ:
            return [*cls.standard_config_files]
        return [os.path.expanduser(f)
                for f in os.environ['DOCUTILSCONFIG'].split(os.pathsep)
                if f.strip()]

    def get_default_values(self):
        """Needed to get custom `_Namespace` instances."""
        defaults = {**self.arg_defaults, "_config_files": self.config_files}
        return Values(**defaults)

    def get_option_by_dest(self, dest):
        """
        Get an option by its dest.

        If you're supplying a dest which is shared by several options,
        it is undefined which option of those is returned.

        A KeyError is raised if there is no option with the supplied
        dest.
        """
        for group in (*self._action_groups, self):
            for option in group._actions:
                if option.dest == dest:
                    return option
        raise KeyError(f'No option with dest == {dest!r}.')


def _create_option(
        group, help_text, option_strings, kwargs, arg_defaults, list_args
):
    # Dynamically create callback action
    if kwargs.get("action") == "callback":
        kwargs.pop('action')
        callback = kwargs.pop("callback")
        callback_args = kwargs.pop('callback_args', "")

        class _Action(_LegacyCallbackAction):
            _legacy_callable = callback
            _callback_args = callback_args
        kwargs["action"] = _Action

    # fix type argument
    if kwargs.get("type") == "string":
        kwargs["type"] = str
    if kwargs.get("type") == "int":
        kwargs["type"] = int

    if kwargs.get("validator") == validate_encoding_and_error_handler:
        kwargs["action"] = kwargs.pop("validator")

    # fix validator, update to type.
    if "validator" in kwargs:
        validator = kwargs.pop("validator")
        if kwargs.get("action") not in {"store_true", "store_false"}:
            kwargs["type"] = validator
        else:
            assert validator == validate_boolean
    else:
        validator = lambda x: x  # NoQA
    overrides = kwargs.pop("overrides", None)

    option = group.add_argument(*option_strings, help=help_text, **kwargs)

    # set validator and overrides for ConfigParser
    if isinstance(option, validate_encoding_and_error_handler):
        option.validator = _validate_encoding_and_error_handler_config_parser
    else:
        option.validator = validator
    option.overrides = overrides

    # set arg_defaults from defaults. Set arg default if it is unset
    if option.dest not in {"help", "version"} | arg_defaults.keys():
        arg_defaults[option.dest] = kwargs.get("default", None)
    # update arg default if it is defined and equal to none, and
    # it would be non-None if updated
    elif (arg_defaults.get(option.dest, ...) is None
          and kwargs.get("default") is not None):
        arg_defaults[option.dest] = kwargs["default"]

    # add the argument name to the list of list arguments
    if kwargs.get("action") == "append":
        list_args.add(option.dest)


def _merge_with_list_args(first, second, list_args):
    for arg in (list_args & first.keys() & second.keys()):
        first[arg] += second.pop(arg)
    return {**first, **second}


def get_config_file_settings(argparser, config_file, config_files, components,
                             list_args, relative_path_settings):
    """Returns a dictionary containing appropriate config file settings."""
    if not os.path.isfile(config_file):
        return {}
    config_parser = ConfigParser()
    if argparser is None:
        argparser = OptionParser()
    config_files += config_parser.read([config_file], argparser)
    cfg_settings = {s: dict(config_parser.items(s)) for s in config_parser.sections()}
    applied = set()
    settings = {}
    for component in components:
        if not component:
            continue
        section_dependencies = component.config_section_dependencies or ()
        for section in (*section_dependencies, component.config_section):
            if section in applied:
                continue
            applied.add(section)
            sect = cfg_settings.get(section, {})
            settings = _merge_with_list_args(settings, sect, list_args)
    base_path = os.path.dirname(config_file)
    make_paths_absolute(settings, relative_path_settings, base_path)
    return settings


class ConfigParser(configparser.RawConfigParser):
    """Parser for Docutils configuration files.

    See https://docutils.sourceforge.io/docs/user/config.html.

    Option key normalization includes conversion of '-' to '_'.

    Config file encoding is "utf-8". Encoding errors are reported
    and the affected file(s) skipped.

    This class is provisional and will change in future versions.
    """

    old_settings = {
        'pep_stylesheet': ('pep_html writer', 'stylesheet'),
        'pep_stylesheet_path': ('pep_html writer', 'stylesheet_path'),
        'pep_template': ('pep_html writer', 'template')}
    """{old setting: (new section, new setting)} mapping, used by
    `handle_old_config`, to convert settings from the old [options] section.
    """

    old_warning = """
The "[option]" section is deprecated.  Support for old-format configuration
files will be removed in Docutils 0.21 or later.  Please revise your
configuration files.  See <https://docutils.sourceforge.io/docs/user/config.html>,
section "Old-Format Configuration Files".
"""

    not_utf8_error = """\
Unable to read configuration file "%s": content not encoded as UTF-8.
Skipping "%s" configuration file.
"""

    def read(self, filenames, option_parser=None):
        # Currently, if a `docutils.frontend.OptionParser` instance is
        # supplied, setting values are validated.
        if option_parser is not None:
            warnings.warn('frontend.ConfigParser.read(): parameter '
                          '"option_parser" will be removed '
                          'in Docutils 0.21 or later.',
                          PendingDeprecationWarning, stacklevel=2)
        read_ok = []
        if isinstance(filenames, str):
            filenames = [filenames]
        for filename in filenames:
            # Config files are UTF-8-encoded:
            try:
                read_ok += super().read(filename, encoding='utf-8')
            except UnicodeDecodeError:
                sys.stderr.write(self.not_utf8_error % (filename, filename))
                continue
            if 'options' in self:
                self.handle_old_config(filename)
            if option_parser is not None:
                self.validate_settings(filename, option_parser)
        return read_ok

    def handle_old_config(self, filename):
        warnings.warn_explicit(self.old_warning, ConfigDeprecationWarning,
                               filename, 0)
        options = self.get_section('options')
        if not self.has_section('general'):
            self.add_section('general')
        for key, value in options.items():
            if key in self.old_settings:
                section, setting = self.old_settings[key]
                if not self.has_section(section):
                    self.add_section(section)
            else:
                section = 'general'
                setting = key
            if not self.has_option(section, setting):
                self.set(section, setting, value)
        self.remove_section('options')

    def validate_settings(self, filename, option_parser):
        """
        Call the validator function and implement overrides on all applicable
        settings.
        """
        for section in self.sections():
            for setting in self.options(section):
                try:
                    option = option_parser.get_option_by_dest(setting)
                except KeyError:
                    continue
                if option.validator:
                    value = self.get(section, setting)
                    try:
                        new_value = option.validator(value)
                    except TypeError:
                        new_value = option.validator(value, setting, section, self)
                    except Exception as err:
                        raise ValueError(
                            f'Error in config file "{filename}", '
                            f'section "[{section}]":\n'
                            f'    {docutils.io.error_string(err)}\n'
                            f'        {setting} = {value}')
                    self.set(section, setting, new_value)
                if option.overrides:
                    self.set(section, option.overrides, None)

    def optionxform(self, optionstr):
        """
        Lowercase and transform '-' to '_'.

        So the cmdline form of option names can be used in config files.
        """
        return optionstr.lower().replace('-', '_')

    def get_section(self, section):
        """
        Return a given section as a dictionary.

        Return empty dictionary if the section doesn't exist.

        Deprecated. Use the configparser "Mapping Protocol Access" and
        catch KeyError.
        """
        warnings.warn('frontend.OptionParser.get_section() '
                      'will be removed in Docutils 0.22 or later.',
                      PendingDeprecationWarning, stacklevel=2)
        try:
            return dict(self[section])
        except KeyError:
            return {}

class ConfigDeprecationWarning(FutureWarning):
    """Warning for deprecated configuration file features."""


def get_default_settings(*components):
    """Get default settings for the OptionParser.

    If passed SettingsSpec subclasses, the default settings from these
    components are included as well.

    """
    return OptionParser(components).get_default_values()
