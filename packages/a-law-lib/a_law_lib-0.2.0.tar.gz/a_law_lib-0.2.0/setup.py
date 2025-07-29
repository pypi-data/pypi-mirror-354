from setuptools import setup, find_packages
with open("README.md","r") as f:
    description= f.read()


setup(
    name='a_law_lib',
    version='0.2.0',
    description='A-law companding and quantization processing for WAV audio files',
    author='Akshaya Krishna R',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.6',
    long_description=description,
    long_description_content_type="text/markdown",
)
