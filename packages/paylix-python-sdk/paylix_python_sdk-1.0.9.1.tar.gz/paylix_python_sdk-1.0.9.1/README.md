# Paylix Python SDK 

![tag](https://img.shields.io/github/v/tag/paylix/python-sdk?sort=date&color=blueviolet)
![pypi](https://img.shields.io/pypi/v/paylix-python-sdk)
![Downloads](https://static.pepy.tech/badge/paylix-python-sdk)

## Introduction

Paylix public API for developers to access merchant resources

## Requirements

- python ^3.7

## Installation

Install the package through pip.

```
python3 -m pip install paylix-python-sdk
```

## Usage

```python
from paylix import Paylix

# pass <MERCHANT_NAME> only if you need to be authenticated as an additional store

client = Paylix("<YOUR_API_KEY>", "<MERCHANT_NAME>")

try:
    products = client.get_products()
except Paylix.PaylixException as e:
    print(e)

```

## Documentation

[Paylix Developers API](https://developers.paylix.gg)
