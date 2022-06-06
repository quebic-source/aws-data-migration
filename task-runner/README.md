### Setup virtual environment
### Install dependencies
* pip3 install -r requirments.txt

## Prepare for deploy
* Deactivate the virtual environment
* cd <virtual-envirment-path>/site-packages 
```shell
cd venv/lib/python3.10/site-packages
```
* Create a deployment package with the installed libraries at the root
```shell
zip -r ../../../../my-deployment-package.zip .
```
* Add function code files to the root of your deployment package
```shell
# jump project root
cd ../../../../ 
zip -g my-deployment-package.zip main.py
```

## AWS Lambda
* name - txtlee-be-dev-web-text-extractor
* handler - main.handler

