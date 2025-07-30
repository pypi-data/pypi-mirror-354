#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import os
import re

with open('cool_qrcode/__init__.py', 'r', encoding='utf-8') as f:
    version = re.search(r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read()).group(1)

with open('README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

setup(
    name='cool-qrcode',
    version=version,
    description='一个用于生成个性化二维码的Python库',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Kelvin Xu',
    author_email='xxk59@hotmail.com',
    url='https://github.com/xxk59/cool-qrcode',
    packages=find_packages(),
    install_requires=[
        'Pillow>=9.0.0',
        'qrcode>=7.0.0',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='qrcode, qr, cool-qrcode, 二维码',
    python_requires='>=3.7',
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'black>=22.0.0',
            'isort>=5.0.0',
        ],
    },
) 