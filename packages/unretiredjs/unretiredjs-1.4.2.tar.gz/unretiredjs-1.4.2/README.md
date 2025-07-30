# UnretiredJS

A Python port of [RetireJS](https://github.com/RetireJS/retire.js) - A tool to scan for vulnerabilities in JavaScript libraries.

[![PyPI](https://img.shields.io/pypi/v/unretiredjs.svg?style=flat-square)](https://pypi.org/project/unretiredjs/)
[![PyPI](https://img.shields.io/pypi/dm/unretiredjs.svg?style=flat-square)](https://pypi.org/project/unretiredjs/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg?style=flat-square)](LICENSE)

## Description

UnretiredJS is a Python library that helps you identify known vulnerabilities in JavaScript libraries used in your web applications. It's a port of the popular RetireJS tool, bringing the same powerful vulnerability scanning capabilities to Python projects.

> **Note**: This is a fork of [FallibleInc/retirejslib](https://github.com/FallibleInc/retirejslib), maintained and updated with additional features and improvements.

## Installation

```bash
pip install unretiredjs
```

## Usage

### Basic Usage

```python
import unretiredjs

# Scan a remote JavaScript file
results = unretiredjs.scan_endpoint("http://code.jquery.com/jquery-1.6.min.js")
```

### Sample Output

```python
[
    {
        'detection': 'filecontent',
        'vulnerabilities': [
            {
                'info': [
                    'http://web.nvd.nist.gov/view/vuln/detail?vulnId=CVE-2011-4969',
                    'http://research.insecurelabs.org/jquery/test/'
                ],
                'identifiers': {
                    'CVE': ['CVE-2011-4969']
                },
                'severity': 'medium'
            },
            {
                'info': [
                    'http://bugs.jquery.com/ticket/11290',
                    'http://research.insecurelabs.org/jquery/test/'
                ],
                'identifiers': {
                    'bug': '11290',
                    'summary': 'Selector interpreted as HTML'
                },
                'severity': 'medium'
            },
            {
                'info': [
                    'https://github.com/jquery/jquery/issues/2432',
                    'http://blog.jquery.com/2016/01/08/jquery-2-2-and-1-12-released/'
                ],
                'identifiers': {
                    'summary': '3rd party CORS request may execute'
                },
                'severity': 'medium'
            }
        ],
        'version': '1.6.0',
        'component': 'jquery'
    }
]
```

## Features

- Scan remote JavaScript files for known vulnerabilities
- Detect vulnerable versions of popular JavaScript libraries
- Comprehensive vulnerability database
- Easy to integrate into Python projects

## Requirements

- Python 3.6 or higher
- requests>=2.25.0

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Anand Kumar - [GitHub](https://github.com/Anandseth444)