# Python Tips & Tricks

Some Tips and Tricks about Python.

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)  [![forthebadge](https://forthebadge.com/images/badges/contains-technical-debt.svg)](http://forthebadge.com)  [![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)](http://forthebadge.com)  [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](http://forthebadge.com)

![Python](./images/python-logo-256.png)

## Useful documents

* [BeautifulSoup overview](./scripts/XmlParser.py) - An overview of BeautifulSoup library, in order to parse XML files.
* [VB inspection](./scripts/Oletools.py)

## Useful links

* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [OleTools](http://www.decalage.info/python/oletools) - Tools developed in Python to analyze OLE files and Microsoft Office files

## Build with

* [Python](https://www.python.org/) - Programming language
* [Docker](https://www.docker.com/) - Set of platform as a service (PaaS) products that use OS-level virtualization to deliver software in packages called containers
* [Git](https://git-scm.com) - Open source distributed version control system
* [PostgreSQL](https://www.postgresql.org) - Open source object-relational database system

## Get started with Oletools

This script aims to inspect the VB code present in the Excel files.

This allows you to quickly have an overview of the code present in these files and to hunt down "wild" extractions, CRUD operations via OLEDB or ODBC connections, ...

1. Install Python (if you haven't already)
2. Clone this repository
3. Install OleTools

```bat
pip install -U oletools
```

4. Configure the scan (directory & file pattern) through the oletools.ini file
5. Excecute Oletools.py

```bat
Python Oletools.py
```

The script will expose in the /out/result.log folder the VBA contents of each scanned file.
Analysis logs are available in the /log/vba-inspect.log folder

## Contributing

If you would like to contribute, read the CONTRIBUTING.md file to learn how to do so.