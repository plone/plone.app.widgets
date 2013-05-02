from lxml import etree
from zope.interface import implements
from zope.interface import implementer
from zope.interface import implementsOnly
from zope.interface import Interface
from zope.component import adapts
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.schema import TextLine
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import ITextLine
from zope.schema.interfaces import ITuple
from zope.schema.interfaces import ISequence
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

    pattern_el_type = 'select'
    pattern_name = 'select2'

    width = '20em'

    def customize_widget(self, widget, value):

        if self.width:
            widget.options['width'] = self.width
        items = self.items
        if callable(items):
            items = items()
        for item in items:
            option = etree.Element('option')
            option.attrib['value'] = item['value']
            if item['selected']:
                option.attrib['selected'] = 'selected'
            option.text = item['content']
            widget.el.append(option)


class ITagsWidget(IWidget):

    width = TextLine()
    ajax_suggest = TextLine()


class TagsWidget(PatternsWidget, Widget):

    implementsOnly(ITagsWidget)

    pattern_name = 'select2'

    width = '30em'
    separator = ';'
    ajax_suggest = ''

    def customize_widget(self, widget, value):

        if self.width:
            widget.options['width'] = self.width

        if self.separator:
            widget.options['separator'] = self.separator

        if self.ajax_suggest:
            state = getMultiAdapter(
                (self.context, self.request), name=u'plone_portal_state')
            widget.options['ajax_suggest'] = state.portal_url() + \
                '/@@widgets/getVocabulary?name=' + self.ajax_suggest

        try:
            widget.el.attrib['value'] = value
        except:
            # FIXME: encoding shouldn't be hardcoded
            widget.el.attrib['value'] = value.decode('utf-8')
        widget.el.attrib['type'] = 'text'


class TagsWidgetConverter(BaseDataConverter):
    """Data converter for ITextLinesWidget."""

    adapts(ISequence, ITagsWidget)

    def toWidgetValue(self, value):
        """Convert from text lines to HTML representation."""
        if value in self.field.missing_value:
            return u''
        return self.widget.separator.join(unicode(v) for v in value)

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
        return collectionType(valueType(v)
                              for v in value.split(self.widget.separator))


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
