with open('functional/tests/_standalone_rst_defaults.py') as _f:
    exec(_f.read())

# Source and destination file names.
test_source = "standalone_rst_manpage.rst"
test_destination = "standalone_rst_manpage.man"

# Keyword parameters passed to publish_file.
writer_name = "manpage"
