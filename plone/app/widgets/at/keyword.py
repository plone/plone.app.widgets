import json
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import KeywordWidget as Base


class KeywordWidget(Base):
    _properties = Base._properties.copy()
    _properties.update({
        'macro': 'keyword',
        'vocabulary': 'plone.app.vocabularies.Keywords',
        'helper_js': (),
        'helper_css': (),
    })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')

    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        fieldName = field.getName()

        tags = [item.strip() for item in json.loads(form.get(fieldName))]
        tags = list(set(tags))

        return tags, {}
