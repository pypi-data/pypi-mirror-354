"""
The setup configuration.
"""

from pathlib import Path

from setuptools import setup, find_packages

setup(
    name='pyavro-gen',
    version_format='{tag}',
    description='A typed class generator for Avro Schemata',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    keywords=['avro', 'classes', 'typing', 'types', 'type', 'typed', 'generation', 'creation',
              'schema', 'schemas', 'schemata'],
    url='https://gitlab.com/Jaumo/pyavro-gen',
    author='Jaumo GmbH',
    author_email='nicola.bova@jaumo.com',
    packages=find_packages(),
    scripts=[
        'pyavro_gen/pyavrogen.py',
    ],
    license='Apache2',
    install_requires=[
        'networkx>=2.8.7',
        'pygments>=2.13.0',
        'factory_boy>=3.2.1',
        'undictify>=0.11.3',
        'faker>=15.1.1',
        'isort>=5.10.1',
        'avro-preprocessor>=0.1.12',
        'pytz>=2022.5',
        'dataclasses-avroschema>=0.37.1'
    ],
)
