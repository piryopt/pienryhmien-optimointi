# Jakaja application architecture

**Customer**
Faculty of Educational Sciences, University of Helsinki

**Source code and documentation:**
[Github repository](https://github.com/piryopt/pienryhmien-optimointi)

## Introduction

The Jakaja application is designed for the Faculty of Educational Sciences of the University of Helsinki. The customer's challenge is assigning large numbers of students into groups. In the past the group assignment was handled manually with Excel sheets, being slow and tedious. Freely available application solutions are not suitable for large groups and it's difficult to take exceptions into account. The Jakaja application is designed to fix the issue.

## Languages and techniques

- Python 
- HTML
- JavaScript
- CSS
- RobotFramework
- Dockerfile


## Libraries and dependencies

| Library | Version | Description |
| ----------- | ----------- | ----------- |
| astroid | 2.15.5| An abstract syntax tree for Python with inference support.| 
| async-generator | 1.10| Async generators and context managers for Python 3.5+ | 
| attrs | 23.1.0| Classes Without Boilerplate | 
| blinker | 1.6.2| Fast, simple object-to-object and broadcast signaling | 
| certifi | 2023.7.22| Python package for providing Mozilla's CA Bundle. | 
| cffi | 1.15.1| Foreign Function Interface for Python calling C code. | 
| click | 8.1.3| Composable command line interface toolkit | 
| colorama | 0.4.6| Cross-platform colored terminal text. | 
| contourpy | 1.1.0| Python library for calculating contours of 2D quadrilateral grids | 
| coverage | 7.2.7| Code coverage measurement for Python | 
| cycler | 0.11.0| Composable style cycles | 
| dill | 0.3.6| serialize all of python | 
| et-xmlfile | 1.1.0| An implementation of lxml.xmlfile for the standard library | 
| exceptiongroup | 1.1.1| Backport of PEP 654 (exception groups) | 
| flask | 2.3.2| A simple framework for building complex web applications. | 
| flask-apscheduler | 1.12.4| Adds APScheduler support to Flask | 
| flask-sqlalchemy | 3.0.5| Add SQLAlchemy support to your Flask application. | 
| fonttools | 4.40.0| Tools to manipulate font files | 
| greenlet | 2.0.2| Lightweight in-process concurrent programming | 
| h11 | 0.14.0| A pure-Python, bring-your-own-I/O implementation of HTTP/1.1 | 
| idna | 3.4 | Internationalized Domain Names in Applications (IDNA) | 
| importlib-metadata | 6.7.0 | Read metadata from Python packages | 
| importlib-resources  | 5.12.0 | Read resources from Python packages | 
| iniconfig  | 2.0.0 | brain-dead simple config-ini parsing | 
| isort  | 5.12.0 | A Python utility / library to sort Python imports. | 
| itsdangerous  | 2.1.2 | Safely pass data to untrusted environments and back. | 
| jinja2  | 3.1.2 | A very fast and expressive template engine. | 
| kiwisolver  | 1.4.4 | A fast implementation of the Cassowary constraint solver | 
| lazy-object-proxy  | 1.9.0 | A fast and thorough lazy object proxy. | 
| markdown  | 3.4.4 | Python implementation of John Gruber's Markdown. | 
| markupsafe  | 2.1.3 | Safely add untrusted strings to HTML/XML markup. | 
| matplotlib  | 3.7.1 | Python plotting package | 
| mccabe  | 0.7.0 | McCabe checker, plugin for flake8 | 
| numpy  | 1.25.0 | Fundamental package for array computing in Python | 
| openpyxl | 3.1.2| A Python library to read/write Excel 2010 xlsx/xlsm files | 
| outcome | 1.2.0| Capture the outcome of Python function calls. | 
| packaging | 23.1 | Core utilities for Python packages | 
| pillow  | 9.5.0| Python Imaging Library (Fork) | 
| platformdirs | 3.7.0| A small Python package for determining appropriate platform-specific dirs, e.g. a \user data dir\. | 
| pluggy | 1.2.0| plugin and hook calling mechanisms for python | 
| psycopg2-binary | 2.9.6| psycopg2 - Python-PostgreSQL Database Adapter | 
| pycparser | 2.21| C parser in Python | 
| pylint | 2.17.4| python code static checker | 
| pyparsing | 3.1.0| pyparsing module - Classes and methods to define and execute parsing grammars | 
| pysocks | 1.7.1| A Python SOCKS client module. See https://github.com/Anorov/PySocks for more information. | 
| pytest | 7.3.2| pytest: simple powerful testing with Python | 
| python-dateutil | 2.8.2| Extensions to the standard Python datetime module | 
| python-dotenv | 1.0.0| Read key-value pairs from a .env file and set them as environment variables | 
| pytz | 2023.3| World timezone definitions, modern and historical | 
| robotframework | 6.1| Generic automation framework for acceptance testing and robotic process automation (RPA) | 
| robotframework-databaselibrary | 1.2.4| Database utility library for Robot Framework | 
| robotframework-pythonlibcore | 4.1.2| Tools to ease creating larger test libraries for Robot Framework using Python. | 
| robotframework-seleniumlibrary | 6.1.0| Web testing library for Robot Framework | 
| scipy | 1.10.1| Fundamental algorithms for scientific computing in Python | 
| selenium | 4.9.1| | 
| setuptools | 68.0.0| Easily download, build, install, upgrade, and uninstall Python packages | 
| six | 1.16.0| Python 2 and 3 compatibility utilities | 
| astroid | 2.15.5| An abstract syntax tree for Python with inference support. | 
| async-generator | 1.10| Async generators and context managers for Python 3.5+ | 
| attrs | 23.1.0| Classes Without Boilerplate | 
| blinker | 1.6.2| Fast, simple object-to-object and broadcast signaling | 
| certifi | 2023.7.22| Python package for providing Mozilla's CA Bundle. | 
| cffi | 1.15.1| Foreign Function Interface for Python calling C code. | 
| click | 8.1.3| Composable command line interface toolkit | 
| colorama | 0.4.6 | Cross-platform colored terminal text. | 
| contourpy  | 1.1.0 | Python library for calculating contours of 2D quadrilateral grids | 
| coverage  | 7.2.7 | Code coverage measurement for Python | 
| cycler  | 0.11.0 | Composable style cycles | 
| dill  | 0.3.6 | serialize all of python | 
| et-xmlfile  | 1.1.0 | An implementation of lxml.xmlfile for the standard library | 
| exceptiongroup  | 1.1.1 | Backport of PEP 654 (exception groups) | 
| flask  | 2.3.2 | A simple framework for building complex web applications. | 
| flask-apscheduler  | 1.12.4 | Adds APScheduler support to Flask | 
| flask-sqlalchemy  | 3.0.5 | Add SQLAlchemy support to your Flask application. | 
| fonttools  | 4.40.0  | Tools to manipulate font files | 
| greenlet  | 2.0.2 | Lightweight in-process concurrent programming | 
| h11  | 0.14.0 | A pure-Python, bring-your-own-I/O implementation of HTTP/1.1 | 
| idna  | 3.4 | Internationalized Domain Names in Applications (IDNA) | 
| importlib-metadata  | 6.7.0 | Read metadata from Python packages | 
| importlib-resources  | 5.12.0 | Read resources from Python packages | 
| iniconfig | 2.0.0| brain-dead simple config-ini parsing | 
| isort  | 5.12.0 | A Python utility / library to sort Python imports. | 
| itsdangerous  | 2.1.2 | Safely pass data to untrusted environments and back. | 
| jinja2  | 3.1.2 | A very fast and expressive template engine. | 
| kiwisolver  | 1.4.4 | A fast implementation of the Cassowary constraint solver | 
| lazy-object-proxy   | 1.9.0 | A fast and thorough lazy object proxy. | 
| markdown  | 3.4.4 | Python implementation of John Gruber's Markdown. | 
| markupsafe  | 2.1.3 | Safely add untrusted strings to HTML/XML markup. | 
| matplotlib  | 3.7.1 | Python plotting package | 
| mccabe  | 0.7.0 | McCabe checker, plugin for flake8 | 
| numpy  | 1.25.0 | Fundamental package for array computing in Python | 
| openpyxl   | 3.1.2 | A Python library to read/write Excel 2010 xlsx/xlsm files | 
| outcome  | 1.2.0 | Capture the outcome of Python function calls. | 
| packaging  | 23.1 | Core utilities for Python packages | 
| pillow  | 9.5.0 | Python Imaging Library (Fork) | 
| platformdirs  | 3.7.0 | A small Python package for determining appropriate platform-specific dirs, e.g. a \user data dir\. | 
| pluggy  | 1.2.0 | plugin and hook calling mechanisms for python | 
| psycopg2-binary  | 2.9.6 | psycopg2 - Python-PostgreSQL Database Adapter | 
| pycparser  | 2.21 | C parser in Python | 
| pylint   | 2.17.4 | python code static checker | 
| pyparsing  | 3.1.0 | pyparsing module - Classes and methods to define and execute parsing grammars | 
| pysocks  | 1.7.1 | A Python SOCKS client module. See https://github.com/Anorov/PySocks for more information. | 
| pytest  | 7.3.2 | pytest: simple powerful testing with Python | 
| python-dateutil  | 2.8.2 | Extensions to the standard Python datetime module | 
| python-dotenv  | 1.0.0 | Read key-value pairs from a .env file and set them as environment variables | 
| pytz  | 2023.3 | World timezone definitions, modern and historical | 
| robotframework  | 6.1 | Generic automation framework for acceptance testing and robotic process automation (RPA) | 
| robotframework-databaselibrary  | 1.2.4 | Database utility library for Robot Framework | 
| robotframework-pythonlibcore  | 4.1.2 | Tools to ease creating larger test libraries for Robot Framework using Python. | 
| robotframework-seleniumlibrary  | 6.1.0 | Web testing library for Robot Framework | 
| scipy  | 1.10.1 | Fundamental algorithms for scientific computing in Python |  
| selenium  | 4.9.1 | | 
| setuptools  | 68.0.0 | Easily download, build, install, upgrade, and uninstall Python packages | 
| six  | 1.16.0 | Python 2 and 3 compatibility utilities | 
| sniffio  | 1.3.0 | Sniff out which async library your code is running under | 
| sortedcontainers  | 2.4.0 | Sorted Containers -- Sorted List, Sorted Dict, Sorted Set | 
| sqlalchemy  | 2.0.16 | Database Abstraction Library | 
| tomli  | 2.0.1 | A lil' TOML parser | 
| tomlkit  | 0.11.8 | Style preserving TOML library | 
| trio  | 0.22.0 | A friendly Python library for async concurrency and I/O | 
| trio-websocket  | 0.10.3 | WebSocket library for Trio | 
| typing-extensions  | 4.6.3 | Backported and Experimental Type Hints for Python 3.7+ | 
| tzdata  | 2023.3 | Provider of IANA time zone data | 
| tzlocal  | 5.0.1 | tzinfo object for the local timezone | 
| urllib3   | 2.0.3 | HTTP library with thread-safe connection pooling, file post, and more. | 
| werkzeug  | 2.3.6 | The comprehensive WSGI web application library. | 
| wrapt  | 1.15.0 | Module for decorators, wrappers and monkey patching. | 
| wsproto  | 1.2.0 | WebSockets state-machine based protocol implementation | 
| zipp  | 3.15.0 | Backport of pathlib-compatible object wrapper for zip files | 
| sniffio  | 1.3.0 | Sniff out which async library your code is running under | 
| sortedcontainers  | 2.4.0 | Sorted Containers -- Sorted List, Sorted Dict, Sorted Set | 
| sqlalchemy   | 2.0.16| Database Abstraction Library | 
 | tomli  | 2.0.1 | A lil' TOML parser | 
| tomlkit  | 0.11.8 | Style preserving TOML library | 
| trio  | 0.22.0 | A friendly Python library for async concurrency and I/O | 
| trio-websocket  | 0.10.3 | WebSocket library for Trio | 
| typing-extensions  | 4.6.3 | Backported and Experimental Type Hints for Python 3.7+ | 
| tzdata  | 2023.3 | Provider of IANA time zone data | 
| tzlocal  | 5.0.1 | tzinfo object for the local timezone | 
| urllib3  | 2.0.3 | HTTP library with thread-safe connection pooling, file post, and more. | 
| werkzeug  | 2.3.6 | The comprehensive WSGI web application library. | 
| wrapt  | 1.15.0 | Module for decorators, wrappers and monkey patching. | 
| wsproto  | 1.2.0 | WebSockets state-machine based protocol implementation | 
| zipp | 3.15.0 | Backport of pathlib-compatible object wrapper for zip files | 


## Database

The application dabase consists of 8 tables.

![](https://github.com/piryopt/pienryhmien-optimointi/tree/main/documentation/schema.png)

[Database tables description](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/database_docs/database_tables.md)


## Application logic

[Application logic flow chart](https://github.com/piryopt/pienryhmien-optimointi/blob/main/documentation/process_flow_chart.md)


## Accessibility

The Jakaja application follows [Web Content Accessibility Guidelines reguirements](https://www.saavutettavuusvaatimukset.fi/digipalvelulain-vaatimukset/wcag-2-1/) to make it more accessible.

| **Qualities for WCAG Compliance**               | **Description**                                                                                                |
|-----------------------------------------------|----------------------------------------------------------------------------------------------------------------|
| Perceivable Content                           | Present information with alternatives like alt text and captions.   |
| Operable User Interface                       | Provide navigation options for keyboard, mouse, and touch inputs. Ensure clear navigation and manageable time limits. |
| Understandable Information                    | Use clear language, avoid jargon, provide comprehensible error messages, and maintain a consistent layout.       |
| Robust Compatibility                          | Design the app to work well with current technologies, including assistive tools.                  |
| Keyboard Accessibility                        | Ensure all features are usable via keyboard navigation alone.       |             |
| Contrast and Color                            | Maintain sufficient contrast between text and background, and avoid conveying information solely through color. |
| Readable Fonts and Layouts                    | Use of legible and resizable fonts, and design layouts that adapt to different screen sizes and orientations.    |
| Focus and Navigation                          | Clearly indicate keyboard focus and ensure smooth navigation through interactive elements.                   |
| No Keyboard Traps                             | Prevent users from getting stuck in keyboard traps where they can't navigate away using keyboard alone.     |
| Consistent and Predictable Navigation         | Maintain consistent user interface elements for predictable navigation across different sections and pages.  |
| Accessible Forms                              | Design forms with clear labels, proper grouping, and instructions for accurate user input.                 |
