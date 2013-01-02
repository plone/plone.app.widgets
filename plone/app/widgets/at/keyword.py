from Products.Archetypes.Widget import KeywordWidget as Base


class KeywordWidget(Base):
    _properties = Base._properties.copy()
    _properties.update({
        'macro': 'keyword',
        'helper_js': (),
        'helper_css': (),
    })
