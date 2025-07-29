from setuptools import setup, find_packages


setup(
    name='keyvomit',
    version='1.0.1',
    description='Unhinged character sequence generator for passwords, tokens, and general chaos.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='mosphox',
    author_email='mosphox@gmail.com',
    url='https://github.com/mosphox/keyvomit',
    project_urls={
        "Source": "https://github.com/mosphox/keyvomit",
        "Tracker": "https://github.com/mosphox/keyvomit/issues"
    },
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'pyperclip'
    ],
    entry_points={
        'console_scripts': [
            'keyvomit = keyvomit.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Console',
        'Topic :: Security :: Cryptography',
        'Intended Audience :: Developers',
    ],
    include_package_data=True,
    zip_safe=False,
)
