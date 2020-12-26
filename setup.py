from setuptools import find_packages, setup

setup(
    name='chgallery',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask>=1.1.2',
        'sqlalchemy>=1.3.20',
        'flask-wtf>=0.14.3',
        'email-validator>=1.1.2'
        'pillow>=8.0.1',
    ],
)
