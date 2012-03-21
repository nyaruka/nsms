from setuptools import setup, find_packages

setup(
    name='nsms',
    version=__import__('nsms').__version__,
    license="BSD",

    install_requires = [
    ],

    description="Provides a skeleton RapidSMS project using Nyaruka's best practices.",
    long_description=open('README.rst').read(),

    author='Nicolas Pottier',
    author_email='code@nyaruka.com',

    url='http://github.com/nyaruka/nsms',
    download_url='http://github.com/nyaruka/nsms/downloads',

    include_package_data=True,

    packages=['nsms'],
    scripts=['scripts/start-nsms'],

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
