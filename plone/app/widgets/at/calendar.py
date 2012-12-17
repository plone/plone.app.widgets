from Products.Archetypes.Widget import CalendarWidget as Base


class CalendarWidget(Base):
    _properties = Base._properties.copy()
    _properties.update({
        'macro': "pickadate",
        'helper_js': (),
        'helper_css': (),
    })
