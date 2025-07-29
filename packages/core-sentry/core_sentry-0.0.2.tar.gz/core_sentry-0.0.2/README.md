# core-sentry
_______________________________________________________________________________

This project provides a set of common components related to the 
integration with Sentry designed to facilitate tracking errors and 
logs monitoring...


## Execution Environment

### Install libraries
```shell
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment.
```shell
virtualenv --python={{python-version}} .venv
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment.
```shell
source .venv/bin/activate
```

### Install required libraries.
```shell
pip install .
```

### Check tests and coverage...
```shell
python manager.py run-tests
python manager.py run-coverage
```
