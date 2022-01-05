# Source and destination file names.
test_source = "latex_literal_block.rst"
test_destination = "latex_literal_block.tex"

# Keyword parameters passed to publish_file.
reader_name = "standalone"
parser_name = "rst"
writer_name = "latex"

# Extra setting we need
settings_overrides['syntax_highlight'] = 'none'
settings_overrides['stylesheet'] = 'docutils'

settings_overrides['legacy_column_widths'] = True
settings_overrides['use_latex_citations'] = False
