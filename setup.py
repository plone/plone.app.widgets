from setuptools import setup, find_packages

version = '1.3.3'

setup(
    name='plone.app.widgets',
    version=version,
    description="better plone widgets",
    long_description='%s\n%s' % (
        open("README.rst").read(),
        open("CHANGES.rst").read(),
    ),
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='plone widgets z3cform archetypes',
    author='Nathan Van Gheem',
    author_email='vangheem@gmail.com',
    url='https://github.com/plone/plone.app.widgets',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['plone', 'plone.app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        # needed because we use bundles
        'Products.ResourceRegistries>=2.1',
        # nedded because users vocabulary was added here
        'plone.app.vocabularies>=2.1.11',
        # needed for pickadate javascript
        'plone.app.jquery>=1.8.0',
        # needed so it works with jquery >= 1.8
        'plone.app.search>=1.1.2',
        'plone.app.registry>=1.2.2'
    ],
    extras_require={
        'test': [
            'plone.app.testing',
            'mock',
        ],
        'archetypes': [
            'archetypes.schemaextender',
        ],
        'dexterity': [
            'plone.app.dexterity',
            'plone.app.contenttypes'
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
