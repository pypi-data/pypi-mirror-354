from setuptools import setup, find_packages

setup(
    name='reverseword',  # Your package name
    version='0.1.0',     # Version
    author='Your Name',
    author_email='your.email@example.com',
    description='A simple package to reverse words',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/reverseword',  # Optional
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)

