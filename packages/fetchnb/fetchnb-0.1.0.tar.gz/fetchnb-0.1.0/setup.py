from setuptools import setup, find_packages

setup(
    name='fetchnb',
    version='0.1.0',
    description='Fetch code from dontpad.com and write it into a Jupyter Notebook',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Vikas Bhat D',
    author_email='vikasdbhat@gmail.com',
    url='https://github.com/vikas-bhat-d/fetchnb',
    packages=find_packages(),
    install_requires=[
        'requests',
        'nbformat'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
