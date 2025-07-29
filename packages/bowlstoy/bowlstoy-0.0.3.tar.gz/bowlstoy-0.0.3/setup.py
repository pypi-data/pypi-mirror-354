from setuptools import setup

setup(
    name="bowlstoy",
    version="0.0.3",
    author="Bowl",
    author_email="wangdi640@gmail.com",
    description="simple python tool",
    url="",
    packages=["bowlstoy"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'scp>=0.14.4',
        'paramiko>=2.10.3',
        'pyftpdlib>=1.5.6',
        'pysmb>=1.2.9.1',
    ],
    python_requires='>=3.7',
)
