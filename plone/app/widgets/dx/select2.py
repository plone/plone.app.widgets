import json
from lxml import etree
from zope.interface import implements
from zope.interface import implementer
from zope.interface import implementsOnly
from zope.interface import Interface
from zope.component import adapts
from zope.component import adapter
from zope.component import queryUtility
from zope.component import getMultiAdapter
from zope.schema import TextLine
from zope.schema import Tuple
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ITextLine
from zope.schema.interfaces import ITuple
from zope.schema.interfaces import ISequence
from zope.schema.interfaces import IVocabularyFactory
from z3c.form.widget import Widget
from z3c.form.widget import FieldWidget
from z3c.form.converter import BaseDataConverter
from z3c.form.browser.select import SelectWidget as BaseSelectWidget
from z3c.form.interfaces import IWidget
from z3c.form.interfaces import IFieldWidget
from plone.app.widgets.dx.base import PatternsWidget
from plone.app.widgets.interfaces import IWidgetsLayer


class ISelectWidget(IWidget):

    width = TextLine()


class SelectWidget(PatternsWidget, BaseSelectWidget):

    implements(ISelectWidget)

    def __init__(self, *args, **kw):
        super(SelectWidget, self).__init__(*args, **kw)
        self._pattern_options = {}
        self._pattern_el_type = 'select'
        self._pattern_name = 'select2'

        self.width = '20em'

    def render_element(self, el):

        if self.width:
            self._pattern_options['width'] = self.width

        for item in self.items():
            option = etree.Element('option')
            option.attrib['id'] = item['id']
            option.attrib['value'] = item['value']
            if item['selected']:
                option.attrib['selected'] = 'selected'
            option.text = item['content']
            el.append(option)

        return el


class ITagsWidget(IWidget):

    width = TextLine()
    tags = Tuple()
    ajaxtags = TextLine()


class TagsWidget(PatternsWidget, Widget):

    implementsOnly(ITagsWidget)

    def __init__(self, *args, **kw):
        super(TagsWidget, self).__init__(*args, **kw)
        self._pattern_options = {}
        self._pattern_el_type = 'input'
        self._pattern_name = 'select2'

        self.width = '30em'
        self.tags = None
        self.ajaxtags = None

    def render_element(self, el):

        if self.width:
            self._pattern_options['width'] = self.width

        if self.ajaxtags:
            state = getMultiAdapter((self.context, self.request),
                                    name=u'plone_portal_state')
            self._pattern_options['ajaxtags'] = state.portal_url() + \
                '/@@widgets/getVocabulary?name=' + self.ajaxtags

        elif self.tags:
            factory = queryUtility(IVocabularyFactory, self.tags)
            if factory:
                self._pattern_options['tags'] = json.dumps([
                    item.title for item in factory(self.context)])
            else:
                self._pattern_options['tags'] = '[]'

        el.attrib['type'] = 'text'
        el.attrib['value'] = self.value

        return el


class TagsWidgetConverter(BaseDataConverter):
    """Data converter for ITextLinesWidget."""

    adapts(ISequence, ITagsWidget)

    def toWidgetValue(self, value):
        """Convert from text lines to HTML representation."""
        if value in self.field.missing_value:
            return u''
        return u','.join(unicode(v) for v in value)

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        collectionType = self.field._type
        if isinstance(collectionType, tuple):
            collectionType = collectionType[-1]
        if not len(value):
            return self.field.missing_value
        valueType = self.field.value_type._type
        if isinstance(valueType, tuple):
            valueType = valueType[0]
        return collectionType(valueType(v) for v in value.split(','))


@adapter(IChoice, Interface, IWidgetsLayer)
@implementer(IFieldWidget)
def SelectFieldWidget(field, source, request=None):
    """IFieldWidget factory for Select2Widget."""
    # BBB: emulate our pre-2.0 signature (field, request)
    if request is None:
        real_request = source
    else:
        real_request = request
    return FieldWidget(field, SelectWidget(real_request))


@adapter(ITuple, ITextLine, IWidgetsLayer)
@implementer(IFieldWidget)
def TagsFieldWidget(field, value_type, request):
    """IFieldWidget factory for TagsWidget."""
    return FieldWidget(field, TagsWidget(request))
