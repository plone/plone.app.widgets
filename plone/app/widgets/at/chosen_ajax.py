from plone.app.widgets.at.chosen import ChosenWidget


class ChosenAjaxWidget(ChosenWidget):
    _properties = ChosenWidget._properties.copy()
    _properties.update({
        'sortable': 'true',
        'ajax': 'true'
    })

    def __init__(self, *args, **kwargs):
        if 'ajax_rel_url' not in kwargs:
            raise Exception(
                "You must specify a ajax_rel_url for AjaxChosenWidget")
        super(ChosenAjaxWidget, self).__init__(*args, **kwargs)
