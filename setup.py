'''Package description'''
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mkdocs-leanix-plugin',
    version='0.0.0',
    description='A MkDocs plugin to import LeanIX data',
    keywords='mkdocs leanix',
    url='https://github.com/chwebdude/mkdocs-leanix-plugin',
    author='Fabrice Andreis',
    author_email='fabrice@andreis.dev',
    license='MIT',
    python_requires='>=3.6',
    install_requires=[
        'mkdocs>=1.0.4'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'leanix = leanix.plugin:LeanIXPlugin'
        ]
    },

    include_package_data = True,
    long_description_content_type = 'text/markdown',
    long_description = long_description
)
