from setuptools import setup, find_packages

setup(
    name='jssecrets',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            'jssecrets=jssecrets.main:main',
        ],
    },
    author='Diego Espindola',
    description='Tool to find secrets in JavaScript files from a webpage',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/diegoespindola/jsSecrets',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPLv2 License',
    ],
    python_requires='>=3.7',
)