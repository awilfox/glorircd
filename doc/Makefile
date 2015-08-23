all: datastore.html security.html

RST2HTML = rst2html.py  # this is mainly because rst2html5.py is supposed to come Any Day Now™
CSS = addon.css
RST2HTML_FLAGS = --stylesheet=html4css1.css,$(CSS)

datastore.html: datastore.rst $(CSS)
	$(RST2HTML) $(RST2HTML_FLAGS) datastore.rst >datastore.html

security.html: security.rst $(CSS)
	$(RST2HTML) $(RST2HTML_FLAGS) security.rst >security.html
