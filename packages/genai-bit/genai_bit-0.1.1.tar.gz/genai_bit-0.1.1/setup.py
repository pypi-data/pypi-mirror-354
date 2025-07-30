from setuptools import setup, find_packages

setup(
    name='genai_bit',  # Must be globally unique on PyPI
    version='0.1.1',
    packages=find_packages(),
    description='A small library for AI-related sample programs',
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/genai',  # Optional
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
