from setuptools import setup, find_packages

setup(
    name='OTU_predictor',
    version='1.1.0',
    description='Uses a randomForest model to predict which OTUs are present in a microbiome',
    author='Andrew Tedder',
    author_email='a.tedder@bradford.ac.uk',
    packages=find_packages(),
    install_requires=[
        'scikit-learn>=0.24',
        'numpy>=1.21',
        'pandas>=1.3',
        'joblib>=1.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2',
            'tox>=3.24',
            'black>=21.7',
            'flake8>=3.9',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
