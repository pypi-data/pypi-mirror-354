from setuptools import setup, find_packages

setup(
    name='orthpylib',                  
    version='0.1.7',                  
    author='Orthogonal',
    author_email='',
    description='support to get a,b,c,d matrix', 
    long_description=open('README.md').read(), 
    long_description_content_type='text/markdown',
    url='https://github.com/orthogonalpub',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',         
    install_requires=[],       
)
