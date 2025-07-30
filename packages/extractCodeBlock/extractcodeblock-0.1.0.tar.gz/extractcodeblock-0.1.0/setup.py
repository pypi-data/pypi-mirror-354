from setuptools import setup, find_packages

setup(
    name='extractCodeBlock',
    version='0.1.0',
    author='Antick Mazumder',
    author_email='antick.majumder@gmail.com',
    description='A package to extract code blocks from a LLM response, enclosed in triple backticks.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/antick-coder/Extract_LLM_Block_Pkg.git',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)