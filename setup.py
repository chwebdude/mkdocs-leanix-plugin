from setuptools import setup, find_packages


setup(
    name='mkdocs-leanix-plugin',
    version='0.1.0',
    description='A MkDocs plugin to import LeanIX data',
    long_description='Include LeanIX Factsehhets and other stuff',
    keywords='mkdocs leanix',
    url='',
    author='Fabrice Andreis',
    author_email='webdude@duck.com',
    license='MIT',
    python_requires='>=2.7',
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
    }
)
