# Keyword parameters passed to publish_file.
reader_name = "standalone"
parser_name = "rst"

# Settings.
settings_overrides['sectsubtitle_xform'] = 1
settings_overrides['syntax_highlight'] = 'none'

# Source and destination file names.
test_source = "footnotes.txt"
test_destination = "footnotes_html5.html"

# Keyword parameters passed to publish_file.
writer_name = "html5"

# Settings:
# local copy of stylesheets:
# (Test runs in ``docutils/test/``, we need relative path from there.)
settings_overrides['stylesheet_dirs'] = ('.', 'functional/input/data')
settings_overrides['stylesheet_path'] = 'minimal.css,responsive.css'
settings_overrides['footnote_references'] = 'superscript'
settings_overrides['section_self_link'] = True
