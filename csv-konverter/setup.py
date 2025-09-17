from setuptools import setup, find_packages

setup(
    name='csv-konverter',
    version='0.1.0',
    author='Dein Name',
    author_email='deine.email@example.com',
    description='Ein CSV-Konverter, der Volksbank-Exportdateien in das Lexoffice-Format umwandelt.',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'pandas',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)