import os
import re
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(__file__)

PACKAGE_NAME = "Cligo"

SHORT_DESCRIPTION = "A Python CLI Framework."

LONG_DESCRIPTION_FILE_PATH = "README.md"

URL = "https://github.com/AidenEllis/Cligo"

PROJECT_URLS = {
    'Github': 'https://github.com/AidenEllis/Cligo',
    'Documentation': 'https://github.com/AidenEllis/Cligo/blob/main/docs',
    'Issue tracker': 'https://github.com/AidenEllis/Cligo/issues'
}

REQUIREMENTS_FILE_PATH = "requirements.txt"

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

KEYWORDS = [
    "cligo",
    "cli",
    "cli go",
    "python cli framework",
    "CLI Framework",
    "Command Line Interface"
]

AUTHOR = "Aiden Ellis"
AUTHOR_EMAIL = "itsaidenellis@protonmail.com"

try:
    with open(os.path.join(BASE_DIR, 'cligo', '__init__.py')) as f:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
except AttributeError:
    raise RuntimeError("__version__ not found.")

if not version:
    raise RuntimeError('Verison not provided.')


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name=PACKAGE_NAME,
    version=version,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license='MIT',
    long_description_content_type="text/markdown",
    long_description=read_file('README.md'),
    description=SHORT_DESCRIPTION,
    packages=find_packages(),
    url=URL,
    project_urls=PROJECT_URLS,
    install_requires=requirements,
    keywords=KEYWORDS,
    entry_points={
        'console_scripts': [
            "cligo = cligo.core.management:execute_from_command_line",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
