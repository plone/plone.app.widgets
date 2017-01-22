# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup

version = '2.1.1.dev0'

setup(
    name='plone.app.widgets',
    version=version,
    description="better plone widgets",
    long_description='%s\n%s' % (
        open('README.rst').read(),
        open('CHANGES.rst').read(),
    ),
    classifiers=[
        'Framework :: Plone',
        'Framework :: Plone :: 5.0',
        'Framework :: Plone :: 5.1',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='plone widgets z3cform dexterity',
    author='Nathan Van Gheem',
    author_email='vangheem@gmail.com',
    url='https://github.com/plone/plone.app.widgets',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'plone.app.contenttypes>=1.1b1',
        'plone.app.dexterity',
        'plone.app.event>=1.2',
        'plone.app.vocabularies>=2.1.12dev',  # users vocabulary used
        'plone.app.z3cform'
        'Products.CMFPlone>=5.0.dev0',  # compatibility with jQuery 1.9+
        'setuptools',
    ],
    extras_require={
        'test': [
            'mock',
            'plone.app.robotframework[debug]',
            'plone.app.testing>=4.2.4',  # we need ROBOT_TEST_LEVEL
        ],
        'archetypes': [
            # keep this for BBB
            # the following were not used at all
            # anymore
            # ----------------------------------
            # 'DateTime',
            # 'Products.Archetypes',
            # 'archetypes.schemaextender',
        ],
        'dexterity': [
            # keep this for BBB
            # the following were not used at all.
            # -----------------------------------
            # 'pytz',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
