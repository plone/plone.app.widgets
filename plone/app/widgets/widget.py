# -*- coding: utf-8 -*-

from plone.app.widgets.dx import AjaxSelectWidget
from plone.app.widgets.dx import QueryStringWidget
from plone.app.widgets.dx import RelatedItemsWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import FieldWidget
from zope.interface import implementer


@implementer(IFieldWidget)
def RelatedItemsFieldWidget(field, request):
    return FieldWidget(field, AjaxSelectWidget(request))


@implementer(IFieldWidget)
def MultiRelatedItemsFieldWidget(field, request):
    return FieldWidget(field, RelatedItemsWidget(request))


@implementer(IFieldWidget)
def QueryStringFieldWidget(field, request):
    return FieldWidget(field, QueryStringWidget(request))
