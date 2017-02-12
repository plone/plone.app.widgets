from setuptools import setup, find_packages

version = '1.9.1'

setup(
    name='plone.app.widgets',
    version=version,
    description="better plone widgets",
    long_description='%s\n%s' % (
        open("README.rst").read(),
        open("CHANGES.rst").read(),
    ),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Plone',
        'Framework :: Plone :: 4.3',
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
        'setuptools',
        # needed because we use bundles
        'Products.ResourceRegistries>=2.1',
        # nedded because users vocabulary was added here
        'plone.app.vocabularies>=2.1.12dev',
        # needed for compatibility with jQuery 1.9+
        'Products.CMFPlone>=4.3.4',
        'plone.app.registry',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework[debug]',
            'plone.app.testing>=4.2.4',  # we need ROBOT_TEST_LEVEL
            'mock',
        ],
        'archetypes': [
            'DateTime',
            'Products.Archetypes',
            'archetypes.schemaextender',
        ],
        'dexterity': [
            'pytz',
            'plone.app.dexterity',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
