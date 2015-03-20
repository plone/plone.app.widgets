from setuptools import setup, find_packages

version = '2.0.0.dev0'

setup(
    name='plone.app.widgets',
    version=version,
    description="better plone widgets",
    long_description='%s\n%s' % (
        open("README.rst").read(),
        open("CHANGES.rst").read(),
    ),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: JavaScript',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='plone widgets z3cform archetypes',
    author='Nathan Van Gheem',
    author_email='vangheem@gmail.com',
    url='https://github.com/plone/plone.app.widgets',
    packages=find_packages(),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'five.globalrequest',
        'plone.app.layout',
        'plone.app.vocabularies',
        'plone.namedfile',
        'Products.CMFPlone>=5.0.dev0',
        'Products.ResourceRegistries',
        'setuptools',
        'zope.component',
        'zope.interface',
        'zope.schema',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.robotframework[debug]',
            'plone.app.testing',
            'plone.testing',
            'robotsuite',
        ],
        'archetypes': [
            'archetypes.schemaextender',
            'DateTime',
            'Products.Archetypes',
        ],
        'dexterity': [
            'plone.app.dexterity',
            'pytz',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
