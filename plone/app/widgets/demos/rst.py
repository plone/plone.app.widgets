# http://wiki.python.org/moin/ReStructuredText

import docutils.core


def restructured_to_html(s):
    """ Convert RST string to HTML string.
    """

    if not s:
        return s

    parts = docutils.core.publish_parts(source=s, writer_name='html')

    return parts['body_pre_docinfo']+parts['fragment']
