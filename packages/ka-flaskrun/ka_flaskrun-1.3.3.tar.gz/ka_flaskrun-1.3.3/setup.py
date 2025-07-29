from setuptools import setup, find_packages

setup(
    name='ka_flaskrun',
    version='1.3.3',
    description='License verification middleware for Flask apps',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author='Saad EL KAFI',
    author_email='mrsaadkafi@gmail.com',
    url='https://github.com/saadelkafi',  # لاحقًا
    packages=find_packages(),
    install_requires=[
        'flask',
        'requests'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Flask',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
