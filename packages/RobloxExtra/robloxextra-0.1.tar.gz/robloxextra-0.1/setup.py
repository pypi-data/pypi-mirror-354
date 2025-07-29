from setuptools import setup, find_packages

setup(
    name='RobloxExtra',  # must be unique on PyPI
    version='0.1',
    packages=find_packages(),
    description='Roblox Api Function Wrapper',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Carter',
    author_email='carter@email.com',
    url='https://github.com/yourname/yourlib',  # optional
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)
