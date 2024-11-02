# Project Dependencies and Licenses

## Python Dependencies

| Library | License | Link to Source |
|---------|---------|----------------|
| astroid | LGPL-2.1 | https://github.com/pylint-dev/astroid |
| autopep8 | MIT | https://github.com/hhatto/autopep8 |
| bcrypt | Apache-2.0 | https://github.com/pyca/bcrypt |
| black | MIT | https://github.com/psf/black |
| blinker | MIT | https://github.com/pallets/blinker |
| Flask | BSD-3-Clause | https://github.com/pallets/flask |
| Flask-Cors | MIT | https://github.com/corydolphin/flask-cors |
| Flask-PyMongo | BSD | https://github.com/dcrosta/flask-pymongo |
| numpy | BSD-3-Clause | https://github.com/numpy/numpy |
| pandas | BSD-3-Clause | https://github.com/pandas-dev/pandas |
| pylint | GPL-2.0 | https://github.com/pylint-dev/pylint |
| pymongo | Apache-2.0 | https://github.com/mongodb/mongo-python-driver |
| pytest | MIT | https://github.com/pytest-dev/pytest |
| pytest-cov | MIT | https://github.com/pytest-dev/pytest-cov |
| python-dotenv | BSD-3-Clause | https://github.com/theskumar/python-dotenv |
| requests | Apache-2.0 | https://github.com/psf/requests |
| scikit-surprise | BSD-3-Clause | https://github.com/NicolasHug/Surprise |
| scipy | BSD-3-Clause | https://github.com/scipy/scipy |

## React/Node.js Core Dependencies

Since you mentioned you're using React and Node.js, here are the core dependencies you should include in your license documentation:

| Library | License | Link to Source |
|---------|---------|----------------|
| React | MIT | https://github.com/facebook/react |
| React DOM | MIT | https://github.com/facebook/react |
| Node.js | MIT | https://github.com/nodejs/node |
| npm | Artistic-2.0 | https://github.com/npm/cli |

Note: To get a complete list of Node.js dependencies and their licenses, you can:
1. Run `npm list` to see all installed packages
2. Use `npm-license-checker` or similar tools to automatically generate a license report for all Node.js dependencies:
```bash
npm install -g license-checker
license-checker --summary
```