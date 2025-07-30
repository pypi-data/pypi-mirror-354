from setuptools import setup, find_packages

setup(
    name='spam_detector_cli',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'scikit-learn',
        'pandas',
        'joblib',
        'requests'
    ],
    entry_points={
        'console_scripts': [
            'spam-detector=spam_detector.cli:main'
        ]
    },
    author='Boenzoel',
    description='CLI sederhana untuk mendeteksi spam SMS/email.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
