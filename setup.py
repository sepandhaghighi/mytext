# -*- coding: utf-8 -*-
"""Setup module."""
from typing import List
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_requires() -> List[str]:
    """Read requirements.txt."""
    requirements = open("requirements.txt", "r").read()
    return list(filter(lambda x: x != "", requirements.split()))


def read_description() -> str:
    """Read README.md and CHANGELOG.md."""
    try:
        with open("README.md") as r:
            description = "\n"
            description += r.read()
        with open("CHANGELOG.md") as c:
            description += "\n"
            description += c.read()
        return description
    except Exception:
        return '''MyText is a lightweight AI-powered text enhancement tool that rewrites, paraphrases, and adjusts tone using modern LLM providers.
        It offers a clean command-line interface and a minimal Python API, supports multiple providers (Google AI Studio & Cloudflare Workers AI),
        and automatically selects the first available provider based on your environment variables.'''


setup(
    name='mytext',
    packages=['mytext'],
    version='0.4',
    description='MyText: A Minimal AI-Powered Text Rewriting Tool',
    long_description=read_description(),
    long_description_content_type='text/markdown',
    include_package_data=True,
    author='Sepand Haghighi',
    author_email='me@sepand.tech',
    url='https://github.com/sepandhaghighi/mytext',
    download_url='https://github.com/sepandhaghighi/mytext/tarball/v0.4',
    keywords="text rewrite paraphrase editing llm ai text-processing cli",
    project_urls={
        'Source': 'https://github.com/sepandhaghighi/mytext'
    },
    install_requires=get_requires(),
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Other Audience',
        'Topic :: Utilities',
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Text Processing :: General",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    license='MIT',
    entry_points={
        'console_scripts': [
            'mytext = mytext.functions:main',
        ]}
)
