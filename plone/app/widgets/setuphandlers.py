# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


def default(context):
    """."""

    if context.readDataFile('plone.app.widgets_default.txt') is None:
        return

    portal = context.getSite()

    css = getToolByName(portal, 'portal_css')
    css_resources = {}
    for item in css.resources:
        css_resources[item.getId()] = item
    for item in [
            "++resource++plone.formwidget.autocomplete/jquery.autocomplete.css",  # flake8: noqa
            "++resource++plone.formwidget.contenttree/contenttree.css",
            "++resource++plone.formwidget.querystring.querywidget.css"]:
        if item in css_resources.keys():
            css_resources[item].setBundle('deprecated')

    javascript = getToolByName(portal, 'portal_javascripts')
    javascript_resources = {}
    for item in javascript.resources:
        javascript_resources[item.getId()] = item
    for item in [
            "++resource++plone.formwidget.autocomplete/formwidget-autocomplete.js",  # flake8: noqa
            "++resource++plone.formwidget.autocomplete/jquery.autocomplete.min.js",  # flake8: noqa
            "++resource++plone.formwidget.contenttree/contenttree.js",
            "++resource++plone.formwidget.querystring.querywidget.js"]:
        if item in javascript_resources.keys():
            javascript_resources[item].setBundle('deprecated')


def uninstall(context):
    """."""

    if context.readDataFile('plone.app.widgets_uninstall.txt') is None:
        return

    portal = context.getSite()

    css = getToolByName(portal, 'portal_css')
    css_resources = {}
    for item in css.resources:
        css_resources[item.getId()] = item
    for item in [
            "++resource++plone.formwidget.autocomplete/jquery.autocomplete.css",  # flake8: noqa
            "++resource++plone.formwidget.contenttree/contenttree.css",
            "++resource++plone.formwidget.querystring.querywidget.css"]:
        if item in css_resources.keys():
            css_resources[item].setBundle('default')

    javascript = getToolByName(portal, 'portal_javascripts')
    javascript_resources = {}
    for item in javascript.resources:
        javascript_resources[item.getId()] = item
    for item in [
            "++resource++plone.formwidget.autocomplete/formwidget-autocomplete.js",  # flake8: noqa
            "++resource++plone.formwidget.autocomplete/jquery.autocomplete.min.js",  # flake8: noqa
            "++resource++plone.formwidget.contenttree/contenttree.js",
            "++resource++plone.formwidget.querystring.querywidget.js"]:
        if item in javascript_resources.keys():
            javascript_resources[item].setBundle('default')
