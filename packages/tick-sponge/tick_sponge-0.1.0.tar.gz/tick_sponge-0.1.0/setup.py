from setuptools import setup, find_packages

setup(
    name='tick_sponge',
    version='0.1.0',
    description='Downloader for historical tick data',
    author='nasadiya',
    author_email='you@example.com',
    url='https://github.com/nasadiya/tick_data_downloader',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'playwright',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.13.2',
)
