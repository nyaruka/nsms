from setuptools import setup, find_packages

setup(
    name='rsms',
    version=__import__('rsms').__version__,
    license="BSD",

    install_requires = [
        "rapidsms==0.9.6a",
    ],

    description="Provides base RapidSMS implementation using Nyaruka's best practices.",
    long_description=open('README.rst').read(),

    author='Nicolas Pottier',
    author_email='code@nyaruka.com',

    url='http://github.com/nyaruka/rsms',
    download_url='http://github.com/nyaruka/rsms/downloads',

    include_package_data=True,

    packages=['rsms'],
    scripts=['scripts/start-rsms'],

    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)
