# http://wiki.python.org/moin/ReStructuredText

import docutils.core
from docutils.writers.html4css1 import Writer, HTMLTranslator


class HTMLFragmentTranslator(HTMLTranslator):

    def __init__(self, document):
        HTMLTranslator.__init__(self, document)
        self.head_prefix = ['', '', '', '', '']
        self.body_prefix = []
        self.body_suffix = []
        self.stylesheet = []

    def astext(self):
        return ''.join(self.body)


def restructured_to_html(s):
    """ Convert RST string to HTML string.
    """

    if not s:
        return s

    html_fragment_writer = Writer()
    html_fragment_writer.translator_class = HTMLFragmentTranslator
    #html = docutils.core.publish_string(s, writer=html_fragment_writer)

    parts = docutils.core.publish_parts(source=s, writer_name='html')

    return parts['body_pre_docinfo']+parts['fragment']
