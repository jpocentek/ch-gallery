from setuptools import find_packages, setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='chgallery',
    version='0.0.1',
    author='Jakub Pocentek',
    author_email='pocedev@yandex.com',
    description='A simple image gallery',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jpocentek/ch-gallery',
    license_file='LICENSE.txt',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    install_requires=[
        'flask>=1.1.2',
        'sqlalchemy>=1.3.20',
        'flask-wtf>=0.14.3',
        'email-validator>=1.1.2',
        'pillow>=8.0.1',
    ],
)
