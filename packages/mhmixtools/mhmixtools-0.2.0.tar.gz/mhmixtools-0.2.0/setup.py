from setuptools import setup, find_packages

setup(
    name='mhmixtools',
    version='0.2.0',
    packages=find_packages(),
    test_suite='tests',
    install_requires=[
        'requests', 
        'bs4',
        'pillow'
    ],
    author='Md. Mahmud Hasan',
    author_email="mahadymahamudh472@gmail.com",
    description="This package contains various automotion tools",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mahamudh472/mhmixtools.git",   
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],  
)
