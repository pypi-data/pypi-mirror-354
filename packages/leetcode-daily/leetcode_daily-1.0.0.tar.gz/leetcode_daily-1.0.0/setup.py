from setuptools import setup, find_packages

setup(
    name='leetcode_daily',
    entry_points={
        'console_scripts': [
            'leetcode-daily = leetcode_daily.main:main',
        ]
    },
    version='1.0.0',
    author='happydave1',
    packages=find_packages(),
    install_requires=[
        "certifi==2025.4.26",
        "charset-normalizer==3.4.2",
        "idna==3.10",
        "requests==2.32.3",
        "setuptools==80.9.0",
        "urllib3==2.4.0"
    ],
)