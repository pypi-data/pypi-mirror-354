# -*- coding:utf-8 -*-
import os
from setuptools import find_packages, setup
from codecs import open

with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as readme:
    long_description = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="django5-mdeditor",
    version="1.0.1",
    packages=find_packages(
        exclude=["mdeditor_demo", "mdeditor_demo_app.*", "mdeditor_demo_app"]
    ),
    include_package_data=True,
    license="GPL-3.0 License",
    description="A Mdeditor plugin for Django5.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wei-with-two-swords/django5-mdeditor",
    author="wei-with-two-swords",
    author_email="shuangjian_wei@163.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.7",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Framework :: Django :: 2.0",
        "Framework :: Django :: 2.1",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Framework :: Django :: 5.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        # Replace these appropriately if you are stuck on Python 2.
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
