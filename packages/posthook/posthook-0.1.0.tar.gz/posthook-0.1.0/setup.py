from setuptools import setup, find_packages

setup(
    name='posthook',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': [
            'posthook = posthook.cli:cli',
        ],
    },
    author='Your Name',
    description='Jira Git Hook + AI Commit Message Helper',
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
