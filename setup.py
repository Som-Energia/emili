#!/usr/bin/python3
from setuptools import setup

readme = open("README.md").read()

setup(
	name = "emili",
	version = "0.1",
	description = "Mail sending Python/CLI interface using markdown or ANSI codes based content",
	author = "David Garcia Garzon",
	author_email = "voki@canvoki.net",
	url = 'https://github.com/Som-Energia/emili',
	long_description = readme,
	license = 'GNU General Public License v3 or later (GPLv3+)',
    py_modules = "emili.py",
	scripts=[
		'emili.py',
		],
	install_requires=[
        'consolemsg',
		'markdown',
        'deansi',
        'premailer',
	],
	classifiers = [
		'Programming Language :: Python',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 2',
		'Environment :: Console',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Communications :: Email :: Email Clients (MUA)',
		'Topic :: Text Processing :: Markup :: Markdown',
		'Intended Audience :: Developers',
		'Intended Audience :: Science/Research',
		'Development Status :: 5 - Production/Stable',
		'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
		'Operating System :: OS Independent',
	],
)
