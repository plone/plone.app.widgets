import datetime
assert datetime
from plone.app.widgets.formlib import UberRelatedItemWidget
from plone.portlet.collection import collection
from plone.app.portlets.portlets import navigation

collection.AddForm.form_fields['target_collection'].custom_widget = \
    UberRelatedItemWidget
collection.EditForm.form_fields['target_collection'].custom_widget = \
    UberRelatedItemWidget
navigation.AddForm.form_fields['root'].custom_widget = UberRelatedItemWidget
navigation.EditForm.form_fields['root'].custom_widget = UberRelatedItemWidget
