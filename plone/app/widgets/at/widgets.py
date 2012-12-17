from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from DateTime import DateTime


class DefaultValueUtil(object):

    def __init__(self, field, context):
        self.field = field
        self.context = context

    def value(self, accessor):
        return accessor()

    def vocabulary(self):
        return self.field.Vocabulary(self.context)


class ChosenWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()

    _properties.update({
        'macro': "chosen",
        'multi_valued': True,
        'width': 550,
        'widget_util_class': DefaultValueUtil,
        'sortable': 'false',
        'ajax': 'false',
        'ajax_rel_url': '',
        'date': 'false'
    })

    security = ClassSecurityInfo()
    empty_marker = '---NO-VALUE---'

    def ajax_url(self, context):
        rel_url = self.ajax_rel_url
        if rel_url:
            return '%s/%s' % (context.absolute_url(), rel_url)
        return ''

    def value(self, accessor):
        return self.widget_util.value(accessor)

    @property
    def field(self):
        return self.widget_util.field

    def setup(self, field, context):
        self.widget_util = self.widget_util_class(field, context)

    def vocabulary(self, field, context):
        return self.widget_util.vocabulary()

    def translate(self, vocab, value):
        if value in vocab:
            value = vocab.getValue(value)
            # XXX this is silly. Why is the vocabulary value in this format?
            if 'label_at' in value:
                value = ' '.join([v.strip() for v in value.split('label_at')])
        if hasattr(value, 'Title') and callable(value.Title):
            value = value.Title()
        return value

    def in_list(self, value, lst):
        if type(value) in (tuple, list, set):
            value = value[0]
        if len(lst) > 0:
            if type(lst[0]) in (tuple, list, set):
                # only take the first item in the list of tuples
                lst = [i[0] for i in lst]
        else:
            return False
        return value in lst

    def fieldid(self, field):
        return '%s-widget' % field.__name__


class AjaxChosenWidget(ChosenWidget):
    _properties = ChosenWidget._properties.copy()

    _properties.update({
        'sortable': 'true',
        'ajax': 'true'
    })

    def __init__(self, *args, **kwargs):
        if 'ajax_rel_url' not in kwargs:
            raise Exception(
                "You must specify a ajax_rel_url for AjaxChosenWidget")
        super(AjaxChosenWidget, self).__init__(*args, **kwargs)


class DateChosenWidget(ChosenWidget):
    _properties = ChosenWidget._properties.copy()

    _properties.update({
        'multi_valued': False,
        'date': 'true'
        #'chosen_constructure': "jQuery('select#%(id)s').dateChosen(%(options)s);"
    })

    def process_form(self, instance, field, form, empty_marker=None,
                     validating=False):
        fname = field.getName()
        value = form.get(fname, empty_marker)
        # remove empty
        if type(value) in (list, tuple, set):
            new = []
            for v in value:
                if v and v != empty_marker and v != self.empty_marker:
                    new = v
                    break
            value = new
        if not value or value == empty_marker or value == self.empty_marker:
            return empty_marker

        try:
            return DateTime(value), {}
        except SyntaxError:
            return empty_marker
