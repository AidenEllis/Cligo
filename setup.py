from setuptools import setup, find_packages
import os
import subprocess


PACKAGE_NAME = "Cligo"

VERSION_FOLDER_NAME = "cligo"

SHORT_DESCRIPTION = "A Python CLI Framework."

LONG_DESCRIPTION_FILE_PATH = "README.md"

URL = "https://github.com/AidenEllis/Cligo"

PROJECT_URLS = {
  'Github': 'https://github.com/AidenEllis/Cligo'
}

REQUIREMENTS_FILE_PATH = "requirements.txt"

KEYWORDS = [
    "cligo",
    "cli",
    "cli go",
    "python cli framework",
    "CLI Framework",
    "Command Line Interface"
]

AUTHOR = "Aiden"


project_version = subprocess.run(['git', 'describe', '--tags'], stdout=subprocess.PIPE).stdout.decode("utf-8").strip()
assert "." in project_version

assert os.path.isfile(f"{VERSION_FOLDER_NAME}/version.py")

with open(f"{VERSION_FOLDER_NAME}/VERSION", "w", encoding="utf-8") as fh:
    fh.write(f"{project_version}\n")


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name=PACKAGE_NAME,
    version=project_version,
    author=AUTHOR,
    author_email="",
    license='MIT',
    long_description_content_type="text/markdown",
    long_description=read_file('README.md'),
    description=SHORT_DESCRIPTION,
    packages=find_packages(),
    url=URL,
    project_urls=PROJECT_URLS,
    package_data={VERSION_FOLDER_NAME: ['VERSION']},
    install_requires=open(REQUIREMENTS_FILE_PATH).read().split("\n") if REQUIREMENTS_FILE_PATH else [],
    keywords=KEYWORDS,
    classifiers=[
        "Development Status :: 1 - Planning",
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
