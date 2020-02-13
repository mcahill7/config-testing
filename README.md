# config-testing

POC to deploy managed config rule and run integration test against it

## Pipeline
To create the pipeline run the following:
```
aws cloudformation create-stack --stack-name config-testing --template-body file://pipeline/pipeline.yaml --capabilities CAPABILITY_NAMED_IAM
```

## Tests
To run tests locally run the following:
```
pipenv run python -m pytest tests -v
``