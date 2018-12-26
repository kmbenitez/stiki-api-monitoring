# Stiki API Monitoring

> To fix something, you have to know when it's broken

## Description
### api_usage_threshhold_checker
A lambda function deployed on AWS, and run daily. Collects information about remaining API Gateway quota. Sends notification to SNS if quota remaining is less than 5 times the previous day's usage, or less than 10% of overall limit.

## Deployment
I have been using [nficano](https://github.com/nficano)'s [python-lambda](https://github.com/nficano/python-lambda) for deployment.

```
pip install python-lambda
lambda deploy --requirements='requirements.txt'`
```

## Authors

* **Kathleen Benitez** - [PurpleBooth](https://github.com/kmbenitez)

## License

This project is copyright Stiki.
