"""
Generic Docutils command line interface.
"""

import argparse

from docutils.core import publish_cmdline, default_description
from docutils.frontend import ConfigParser, OptionParser

_CONFIG_SECTION = "docutils-cli application"

_config_parser = ConfigParser()
_config_parser.read(OptionParser().get_standard_config_files(), OptionParser())
_config_settings = _config_parser.get_section(_CONFIG_SECTION)

_parser = argparse.ArgumentParser(
    description="Publish documents from reStructuredText or Markdown sources.",
    epilog="Further optional arguments are added by the selected components, "
           "the list below adapts to your selection.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    add_help=False,
)
_parser.add_argument("source", nargs="?")
_parser.add_argument("destination", nargs="?")
_parser.add_argument("-h", "--help", help="show this help message and exit",
                     action="store_true")
_parser.add_argument("-r", "--reader", help="name of the reader",
                     default=_config_settings.get("reader", "standalone"))
_parser.add_argument("-p", "--parser", help="name of the parser",
                     default=_config_settings.get("parser", "rst"))
_parser.add_argument("-w", "--writer", help="name of the writer",
                     default=_config_settings.get("writer", "html5"))


def _publish():
    args, unknown = _parser.parse_known_args()

    if args.help:
        print(_parser.format_help())
        unknown.append("--help")

    try:
        publish_cmdline(
            reader_name=args.reader,
            parser_name=args.parser,
            writer_name=args.writer,
            config_section=_CONFIG_SECTION,
            description=default_description,
            argv=[*filter(None, [args.source, args.destination, *unknown])],
        )
    except ImportError as err:
        if "--traceback" in set(unknown):
            raise err
        print(err)
        raise SystemExit("Use '--traceback' to show details.")


if __name__ == "__main__":
    _publish()
