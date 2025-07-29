from setuptools import setup, find_packages

setup(
    name='knnpy',
    version='0.0.1',
    author='Nisarg Patel',
    author_email='nisargp@maqsoftware.com',
    description='Package for semantic level validation',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
# python setup.py sdist
# twine upload dist/*

#python3 -m build 
#python3 -m  twine upload dist/* 