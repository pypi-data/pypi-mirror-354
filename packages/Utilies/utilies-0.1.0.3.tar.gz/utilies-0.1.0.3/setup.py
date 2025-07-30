from setuptools import setup, find_packages

setup(
    name="Utilies",  # Replace with your package name
    version="0.1.0.3",
    packages=find_packages(),  # Automatically find submodules
    install_requires=[
        "beautifulsoup4==4.13.4",
        "certifi==2024.8.30",
        "markdown-it-py==3.0.0",
        "msal==1.32.3",
        "numpy==2.0.2",
        "o365==2.1.1",
        "oauthlib==3.2.2",
        "openpyxl==3.1.5",
        "pandas==2.2.2",
        "paramiko==3.5.1",
        "pillow==10.4.0",
        "pywin32==306",
        "pywinauto==0.6.8",
        "reportlab==4.2.2",
        "requests==2.32.3",
        "requests-oauthlib==2.0.0",
        "requests-toolbelt==1.0.0",
        "scp==0.15.0",
        "selenium==4.29.0",
        "six==1.16.0",
        "smbprotocol==1.15.0",
        "sniffio==1.3.1",
        "sortedcontainers==2.4.0",
        "XlsxWriter==3.2.0",
        "zipp==3.21.0"
    ]
)
