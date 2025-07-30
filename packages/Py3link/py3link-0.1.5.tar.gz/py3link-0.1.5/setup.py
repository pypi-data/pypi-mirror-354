from setuptools import setup, find_packages

setup(
    name='Py3link',
    version='0.1.5',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pylink = py3link.cli:main',
        ],
    },
    install_requires=[
        'requests',
        'yt-dlp',
        'tqdm',
    ],
    author='MAKCNMOB',
    author_email='mail@example.com',
    description='A powerful and beautiful Python library for downloading files and videos from various sources.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/KinderModddins/py3link',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license='MIT',
    license_file='LICENSE',
)

