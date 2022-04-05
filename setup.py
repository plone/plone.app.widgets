from setuptools import setup, find_packages

version = '4.0.0a1'

setup(
    name='plone.app.widgets',
    version=version,
    description="better plone widgets",
    long_description='%s\n%s' % (
        open("README.rst").read(),
        open("CHANGES.rst").read(),
    ),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords='plone widgets z3cform',
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
        # needed because users vocabulary was added here
        'plone.app.vocabularies>=2.1.12',
        'Products.CMFPlone>=5.2',
        'six',
    ],
    extras_require={
        'test': [
            'plone.app.robotframework[debug]',
            'plone.app.testing>=4.2.4',  # we need ROBOT_TEST_LEVEL
            'mock',
        ],
        'dexterity': [
            'pytz',
            'plone.app.dexterity',
            'plone.app.contenttypes>=1.1',
            'plone.app.event>=1.2',
        ],
    },
    entry_points="""
    # -*- Entry points: -*-
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
