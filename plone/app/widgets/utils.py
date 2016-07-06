# -*- coding: utf-8 -*-
from Acquisition import aq_inner, aq_parent, aq_base
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from datetime import datetime
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.registry.interfaces import IRegistry
from plone.uuid.interfaces import IUUID
from z3c.form.interfaces import IForm
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import providedBy
from zope.component import queryUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import MessageFactory
from zope.schema.interfaces import IVocabularyFactory
import json

_ = MessageFactory('plone.app.widgets')
_plone = MessageFactory('plone')


try:
    from plone.app.event import base as pae_base
    HAS_PAE = True
except ImportError:
    HAS_PAE = False


def first_weekday():
    if HAS_PAE:
        wkday = pae_base.wkday_to_mon1(pae_base.first_weekday())
        if wkday > 1:
            return 1  # Default to Monday
        return wkday
    else:
        cal = getToolByName(getSite(), 'portal_calendar', None)
        if cal:
            wkday = cal.firstweekday
            if wkday == 6:  # portal_calendar's Sunday is 6
                return 0  # Sunday
        return 1  # other cases: Monday


class NotImplemented(Exception):

    """Raised when method/property is not implemented"""


def pickadate_options():
    registry = getUtility(IRegistry)
    options = registry.get('plone.patternoptions', {}).get('pickadate', u'{}')
    return json.loads(options)


def get_date_options(request):
    calendar = request.locale.dates.calendars['gregorian']
    today = datetime.today()
    d_options = pickadate_options().get('date', {})
    y_min = d_options.get('min', 100)
    y_max = d_options.get('max', 20)
    return {
        'time': False,
        'date': {
            'firstDay': calendar.week.get('firstDay') == 1 and 1 or 0,
            'weekdaysFull': [
                calendar.days.get(t, (None, None))[0]
                for t in (7, 1, 2, 3, 4, 5, 6)],
            'weekdaysShort': [
                calendar.days.get(t, (None, None))[1]
                for t in (7, 1, 2, 3, 4, 5, 6)],
            'monthsFull': calendar.getMonthNames(),
            'monthsShort': calendar.getMonthAbbreviations(),
            'selectYears': d_options.get('selectYears', 200),
            'min': [today.year - y_min, 1, 1],
            'max': [today.year + y_max, 1, 1],
            'format': translate(
                _('pickadate_date_format', default='mmmm d, yyyy'),
                context=request),
            'placeholder': translate(_plone('Enter date...'), context=request),
            'today': translate(_plone(u"Today"), context=request),
            'clear': translate(_plone(u"Clear"), context=request),
        }
    }


def get_datetime_options(request):
    t_options = pickadate_options().get('time', {})
    interval = t_options.get('interval', 5)

    options = get_date_options(request)
    options['time'] = {
        'format': translate(
            _('pickadate_time_format', default='h:i a'),
            context=request),
        'placeholder': translate(_plone('Enter time...'), context=request),
        'today': translate(_plone(u"Today"), context=request),
        'interval': interval,
    }
    return options


def get_ajaxselect_options(context, value, separator, vocabulary_name,
                           vocabulary_view, field_name=None):
    options = {'separator': separator}
    if vocabulary_name:
        options['vocabularyUrl'] = '{}/{}?name={}'.format(
            get_context_url(context), vocabulary_view, vocabulary_name)
        if field_name:
            options['vocabularyUrl'] += '&field={}'.format(field_name)
        if value:
            vocabulary = queryUtility(IVocabularyFactory, vocabulary_name)
            if vocabulary:
                options['initialValues'] = {}
                vocabulary = vocabulary(context)
                # Catalog
                if vocabulary_name == 'plone.app.vocabularies.Catalog':
                    uids = value.split(separator)
                    try:
                        catalog = getToolByName(context, 'portal_catalog')
                    except AttributeError:
                        catalog = getToolByName(getSite(), 'portal_catalog')
                    for item in catalog(UID=uids):
                        options['initialValues'][item.UID] = item.Title
                else:
                    for value in value.split(separator):
                        try:
                            term = vocabulary.getTerm(value)
                            options['initialValues'][term.token] = term.title
                        except LookupError:
                            options['initialValues'][value] = value
    return options


def get_relateditems_options(context, value, separator, vocabulary_name,
                             vocabulary_view, field_name=None, widget=None):
    options = get_ajaxselect_options(context, value, separator,
                                     vocabulary_name, vocabulary_view,
                                     field_name)
    if IForm.providedBy(context):
        context = context.context
    request = getattr(context, 'REQUEST')
    msgstr = translate(_plone(u'Search'), context=request)
    options.setdefault('searchText', msgstr)
    msgstr = translate(_(u'Entire site'), context=request)
    options.setdefault('searchAllText', msgstr)
    msgstr = translate(_plone('tabs_home',
                              default=u'Home'),
                       context=request)
    options.setdefault('homeText', msgstr)

    if getattr(widget, 'selectable_types', None):
        options['selectableTypes'] = widget.selectable_types

    nav_root = getNavigationRootObject(context, get_portal())
    options['rootPath'] = (
        '/'.join(nav_root.getPhysicalPath()) if nav_root else '/'
    )

    return options


def get_querystring_options(context, querystring_view):
    portal_url = get_portal_url(context)
    try:
        base_url = context.absolute_url()
    except AttributeError:
        base_url = portal_url
    return {
        'indexOptionsUrl': '{}/{}'.format(portal_url, querystring_view),
        'previewURL': '%s/@@querybuilder_html_results' % base_url,
        'previewCountURL': '%s/@@querybuildernumberofresults' % base_url
    }


def get_tinymce_options(context, field, request):
    options = {}

    utility = getToolByName(aq_inner(context), 'portal_tinymce', None)
    if utility:
        # Plone 4.3
        # map Products.TinyMCE settings meant for TinyMCE 3 to version 4
        # see http://www.tinymce.com/wiki.php/Tutorial:Migration_guide_from_3.x
        # and https://github.com/plone/plone.app.widgets/issues/72
        config = utility.getConfiguration(context=context,
                                          field=field,
                                          request=request)

        if config['content_css'] == "":
            config['content_css'] = '++resource++plone.app.widgets-tinymce-content.css'  # noqa

        # FIXME: this might be needed in order to still load/support
        # custom plugins such as collective.tinymceplugins.*
        del config['customplugins']

        # remove theme settings
        del config['theme']

        # override config plugins settings
        # XXX: the list of loaded plugins may change in plone-mockup
        config['plugins'] = [
            'advlist',
            'autolink',
            'lists',
            'charmap',
            'print',
            'preview',
            'anchor',
            'searchreplace',
            'visualblocks',
            'code',
            'fullscreen',
            'insertdatetime',
            'media',
            'table',
            'contextmenu',
            'paste',
            'plonelink',
            'ploneimage',
            'textcolor',
        ]

        # FIXME: map old names to new names in the configuration for plone5
        # and notify migration-team
        # http://www.tinymce.com/wiki.php/Controls
        # also check for buttons no longer available, such as definitionlist
        all_buttons = [
            'advhr',
            'anchor',
            'attribs',
            'backcolor',
            'bold',
            'bullist',
            'charmap',
            'cleanup',
            'code',
            'copy',
            'cut',
            'definitionlist',
            'emotions',
            'forecolor',
            'fullscreen',
            'hr',
            'image',
            'indent',
            'insertdate',
            'inserttime',
            'italic',
            'justifycenter',
            'justifyfull',
            'justifyleft',
            'justifyright',
            'link',
            'media',
            'nonbreaking',
            'numlist',
            'outdent',
            'pagebreak',
            'paste',
            'pastetext',
            'pasteword',
            'preview',
            'print',
            'redo',
            'removeformat',
            'replace',
            'save',
            'search',
            'spellchecker',
            'strikethrough',
            'style',
            'sub',
            'sup',
            'tablecontrols',
            'underline',
            'undo',
            'unlink',
            'visualaid',
            'visualchars',
        ]
        button_settings = dict()
        # FIXME: rename buttons in configuration for plone5, these mappings
        # are only done for plone4
        mappings = dict(justifyleft='alignleft',
                        justifycenter='aligncenter',
                        justifyright='alignright',
                        justifyfull='alignjustify',
                        link='plonelink',
                        tablecontrols='table',
                        image='ploneimage',
                        emotions='emoticons',
                        sub='subscript',
                        sup='superscript',
                        visualaid='visualblocks',
                        )
        for button in all_buttons:
            if button in mappings:
                newname = mappings[button]
                button_settings[newname] = button in config[
                    'buttons'] and newname or ''
            else:
                button_settings[button] = button in config[
                    'buttons'] and button or ''

        if 'search' in config['buttons'] or 'replace' in config['buttons']:
            button_settings['searchreplace'] = 'searchreplace'
        else:
            button_settings['searchreplace'] = ''

        if 'insertdate' in config['buttons']\
                or 'inserttime' in config['buttons']:
            button_settings['insertdatetime'] = 'insertdatetime'
        else:
            button_settings['insertdatetime'] = ''

        button_settings['directionality'] = 'attribs' in config[
            'buttons'] and 'ltr rtl' or ''
        
        # enable browser spell check by default:
        config['browser_spellcheck'] = True

        # FIXME: currently save button does not show up
        if 'save' in config['buttons']\
                and getattr(aq_inner(context), 'checkCreationFlag', None):
            if context.checkCreationFlag():
                # hide save button on object creation
                button_settings['save'] = ''

        # these toolbar buttons are not available anymore:
        # pasteword (cleanup is done by pastetext)
        # cleanup
        # definitionlist (plugin missing, might have been plone-specific)

        # these need to be remapped or renamed
        # FIXME: rename plone5 registry attributes + migration for these
        # search replace -> searchreplace
        # insertdate and inserttime -> insertdatetime
        # attribs (has allowed to add dir="ltr" or lang="en) ->
        #   ltr rtl (directionality plugin)
        # visualaid -> visualblocks
        # emotions -> emoticons

        # buttons currently not working (probably plugin not loaded correctly)
        # nonbreaking, pagebreak - do not show up
        # emoticons - does not show up
        # ltr, rtl (directionality plugin) - do not show up
        # spellchecker - button does not show up
        # visualblocks - do not show any additional borders/lines around p / h2
        # visualchars - does not show up
        # nonbreaking and pagebreak - do not show up
        toolbar = '{save} {cut} {copy} {paste} {pastetext} | ' \
            '{undo} {redo} {searchreplace} | styleselect {removeformat} | ' \
            '{bold} {italic} {underline} {strikethrough} {subscript} {superscript} | ' \
            '{forecolor} {backcolor} | ' \
            '{alignleft} {aligncenter} {alignright} {alignjustify} | ' \
            '{bullist} {numlist} {outdent} {indent} | {table} | ' \
            '{ploneimage} {unlink} {plonelink} {anchor} | ' \
            '{charmap} {hr} {insertdatetime} {emoticons} {nonbreaking} {pagebreak} '\
            '{print} {preview} {visualblocks} {visualchars} {directionality} | ' \
            '{code} {fullscreen} spellchecker'.format(**button_settings)
        config['toolbar'] = toolbar

        # Plone 4.x TinyMCE panel defines table format/style title, classname:
        config['table_class_list'] = map(
            lambda pair: {'title': pair[0], 'value': pair[1]},
            [e.strip().split('|') for e in utility.tablestyles.split('\n')]
        )

        # if forecolor/backcolor enabled in buttons, allow paste of color
        # in text from word processing / rich text:
        paste_allow = []
        if 'forecolor' in config['buttons']:
            paste_allow.append('color')
        if 'backcolor' in config['buttons']:
            paste_allow.append('background')
        config['paste_retain_style_properties'] = ' '.join(paste_allow)

        # contextmenu is no longer available, use this setting for menubar
        # FIXME: plone5 rename setting
        # xxx toolbar_external (theme_advanced_toolbar_location not available
        # in tiny 4)
        if not config['contextmenu']:
            config['menubar'] = ''
        else:
            # TODO: would be great to deactivate menuitems in case toolbar
            # button has been deactivated
            # esp makes sense for link and imagedialog, charmap and code-editor
            config['menubar'] = 'edit {table} format tools view insert'.format(
                table=button_settings['table'],
            )

        # map Plone4 TinyMCE "styles" (raw format) to TinyMCE 4 "style_formats"
        # see http://www.tinymce.com/wiki.php/Configuration:style_formats
        p_style_formats = []
        u_styles = utility.styles and utility.styles.strip().split('\n') or []
        for f in u_styles:
            f_parts = f.split("|")
            s_format = dict(title=f_parts[0])
            # XXX: These node-types need review
            if f_parts[1].lower() in ["span", "b", "i"]:
                s_format['inline'] = f_parts[1].lower()
            elif f_parts[1].lower() in [
                    "tr", "th", "dt", "dd", "ol", "ul", "a"
            ]:
                s_format['selector'] = f_parts[1].lower()
            else:
                s_format['block'] = f_parts[1].lower()
            if len(f_parts) > 2:
                s_format['classes'] = f_parts[2]
            p_style_formats.append(s_format)
        if p_style_formats:
            config["style_formats"] = [
                dict(title=u"Plone Styles", items=p_style_formats),
            ]
            # XXX: Maybe there should be an option to merge default styles or
            # not
            config["style_formats_merge"] = "true"

        # respect resizing settings
        config['resize'] = utility.resizing

        if utility.autoresize:
            config['plugins'].append('autoresize')
            config['autoresize_min_height'] = config[
                'theme_advanced_source_editor_height']

        folder = context
        if not IFolderish.providedBy(context):
            folder = aq_parent(context)
        if IPortletAssignmentMapping.providedBy(folder):
            folder = aq_parent(folder)
        if IPloneSiteRoot.providedBy(folder):
            initial = None
        else:
            initial = IUUID(folder, None)
        portal_url = get_portal_url(context)
        nav_root = getNavigationRootObject(context, get_portal())
        folder_path = '/'.join(folder.getPhysicalPath())
        folder_url_relative = folder.absolute_url()[len(portal_url):]

        options = {
            'relatedItems': {
                'vocabularyUrl': '{0}/{1}'.format(
                    portal_url,
                    '@@getVocabulary?name=plone.app.vocabularies.Catalog'
                ),
                'mode': 'browse',
                'basePath': folder_path,
                'rootPath': '/'.join(nav_root.getPhysicalPath()) if nav_root
                            else '/',
            },
            'upload': {
                'initialFolder': initial,
                'currentPath': folder_url_relative,
                'baseUrl': config['document_base_url'],
                'relativePath': '@@fileUpload',
                'uploadMultiple': False,
                'maxFiles': 1,
                'showTitle': False
            },
            'tiny': config,
            # This is for loading the languages on tinymce
            'loadingBaseUrl': '++resource++plone.app.widgets.tinymce',
            'prependToUrl': 'resolveuid/',
            'linkAttribute': 'UID',
            'prependToScalePart': '/@@images/image/',
            'folderTypes': utility.containsobjects.split('\n'),
            'imageTypes': utility.imageobjects.split('\n'),
            'anchorSelector': utility.anchor_selector,
            'linkableTypes': utility.linkable.split('\n')
        }
    else:
        # Plone 5
        # They are set on the body
        pattern_options = getMultiAdapter(
            (context, request, field),
            name="tinymce_settings")()['data-pat-tinymce']
        options = json.loads(pattern_options)
    return options


def get_portal():
    closest_site = getSite()
    if closest_site is not None:
        for potential_portal in closest_site.aq_chain:
            if ISiteRoot in providedBy(potential_portal):
                return potential_portal


def get_portal_url(context):
    portal = get_portal()
    if portal:
        root = getNavigationRootObject(context, portal)
        if root:
            try:
                return root.absolute_url()
            except AttributeError:
                return portal.absolute_url()
        else:
            return portal.absolute_url()
    return ''


def get_context_url(context):
    if IForm.providedBy(context):
        # Use the request URL if we are looking at an addform
        url = context.request.get('URL')
    elif hasattr(context, 'absolute_url'):
        url = context.absolute_url
        if callable(url):
            url = url()
    else:
        url = get_portal_url(context)
    return url


def get_widget_form(widget):
    form = getattr(widget, 'form', None)
    if getattr(aq_base(form), 'parentForm', None) is not None:
        form = form.parentForm
    return form
