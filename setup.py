from setuptools import setup, find_packages

version = '0.1'

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
        'Products.ResourceRegistries>=2.1',
        'Products.CMFPlone>=4.3b1',
        'Products.TinyMCE>1.3b8',
        'plone.app.vocabularies>2.1.8',
        'five.pt',

    ],
    extras_require={
        'test': [
            'plone.app.testing',
        ],
        'archetypes': [
            'archetypes.schemaextender',
        ],
    },
)
