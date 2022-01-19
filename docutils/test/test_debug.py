# from test import DocutilsTestSupport  # before importing docutils!
#
# from docutils.transforms.universal import SmartQuotes
# from docutils.parsers.rst import Parser
# from docutils import frontend
# from docutils import utils
# from docutils.parsers import rst
# from docutils.transforms import universal
#
#
# class TestSmartQuotes(DocutilsTestSupport.CustomTestCase):
#
#     """
#     Output checker for the transform.
#
#     Should probably be called TransformOutputChecker, but I can deal with
#     that later when/if someone comes up with a category of transform test
#     cases that have nothing to do with the input and output of the transform.
#     """
#
#     settings = frontend.OptionParser(components=(rst.Parser,)).get_default_values()
#     settings.report_level = 1
#     settings.halt_level = 5
#     settings.debug = False
#     settings.warning_stream = DocutilsTestSupport.DevNull()
#     unknown_reference_resolvers = ()
#     parser = Parser()
#
#     def test_default(self):
#         settings = self.settings.copy()
#         settings.smart_quotes = True
#         settings.trim_footnote_ref_space = True
#         settings.report = 2  # TODO: why is this ignored when running as main?
#         document = utils.new_document('test data', settings)
#         self.parser.parse(totest_smartquotes_input, document)
#         # Don't do a ``populate_from_components()`` because that would
#         # enable the Transformer's default transforms.
#         document.transformer.add_transforms((SmartQuotes,))
#         document.transformer.add_transform(universal.TestMessages)
#         document.transformer.components['writer'] = self
#         document.transformer.apply_transforms()
#         output = document.pformat()
#         DocutilsTestSupport._compare_output(self, totest_smartquotes_input, output, totest_smartquotes_expected)
#
#     def test_de(self):
#         settings = self.settings.copy()
#         settings.smart_quotes = True
#         settings.trim_footnote_ref_space = True
#         settings.report = 2  # TODO: why is this ignored when running as main?
#         settings.language_code = "de"  # TODO failing to pick up rst language module
#         document = utils.new_document('test data', settings)
#         self.parser.parse(totest_de_smartquotes_input, document)
#         # Don't do a ``populate_from_components()`` because that would
#         # enable the Transformer's default transforms.
#         document.transformer.add_transforms((SmartQuotes,))
#         document.transformer.add_transform(universal.TestMessages)
#         document.transformer.components['writer'] = self
#         document.transformer.apply_transforms()
#         output = document.pformat()
#         DocutilsTestSupport._compare_output(self, totest_de_smartquotes_input, output, totest_de_smartquotes_expected)
#
#     def test_de_locales(self):
#         settings = self.settings.copy()
#         settings.smart_quotes = True
#         settings.trim_footnote_ref_space = True
#         settings.report = 2  # TODO: why is this ignored when running as main?
#         settings.language_code = "de"
#         settings.smartquotes_locales = [('de', u'«»()'), ('nl', u'„”’’')]
#         document = utils.new_document('test data', settings)
#         self.parser.parse(totest_locales_smartquotes_input, document)
#         # Don't do a ``populate_from_components()`` because that would
#         # enable the Transformer's default transforms.
#         document.transformer.add_transform(SmartQuotes)
#         document.transformer.add_transform(universal.TestMessages)
#         document.transformer.components['writer'] = self
#         document.transformer.apply_transforms()
#         output = document.pformat()
#         DocutilsTestSupport._compare_output(self, totest_locales_smartquotes_input, output, totest_locales_smartquotes_expected)
#
#
# totest_smartquotes_input = """\
# .. class:: language-de
#
# German "smart quotes" and 'secondary smart quotes'.
#
# .. class:: language-en-UK-x-altquot
#
# British "primary quotes" use single and
# 'secondary quotes' double quote signs.
#
# .. class:: language-foo
#
# "Quoting style" for unknown languages is 'ASCII'.
#
# .. class:: language-de-x-altquot
#
# Alternative German "smart quotes" and 'secondary smart quotes'.
# """
# totest_smartquotes_expected = """\
# <document source="test data">
#     <paragraph classes="language-de">
#         German „smart quotes“ and ‚secondary smart quotes‘.
#     <paragraph classes="language-en-uk-x-altquot">
#         British ‘primary quotes’ use single and
#         “secondary quotes” double quote signs.
#     <paragraph classes="language-foo">
#         "Quoting style" for unknown languages is 'ASCII'.
#     <paragraph classes="language-de-x-altquot">
#         Alternative German »smart quotes« and ›secondary smart quotes‹.
#     <system_message level="2" line="12" source="test data" type="WARNING">
#         <paragraph>
#             No smart quotes defined for language "foo".
# """
#
# totest_de_smartquotes_input = """\
# German "smart quotes" and 'secondary smart quotes'.
#
# .. class:: language-en
#
# English "smart quotes" and 'secondary smart quotes'.
# """
# totest_de_smartquotes_expected = """\
# <document source="test data">
#     <paragraph>
#         German „smart quotes“ and ‚secondary smart quotes‘.
#     <paragraph classes="language-en">
#         English “smart quotes” and ‘secondary smart quotes’.
# """
#
# totest_locales_smartquotes_input = """\
# German "smart quotes" and 'secondary smart quotes'.
#
# .. class:: language-nl
#
# Dutch "smart quotes" and 's Gravenhage (leading apostrophe).
# """
# totest_locales_smartquotes_expected = u"""\
# <document source="test data">
#     <paragraph>
#         German «smart quotes» and (secondary smart quotes).
#     <paragraph classes="language-nl">
#         Dutch „smart quotes” and ’s Gravenhage (leading apostrophe).
# """
