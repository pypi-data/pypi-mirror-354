from setuptools import setup, find_packages

setup(
    name='eng2urdu',
    version='0.1.0',
    description='English to Urdu Number Converter',
    packages=find_packages(),
    long_description=open('README.md',encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Wahaj Ali',
    author_email='wahaj0574@gmail.com',
    url='https://github.com/wahaj67/ENG2Urdu-Convertor-Package.git',
  classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
],

    python_requires='>=3.6'
)