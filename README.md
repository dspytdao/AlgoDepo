# AlgoDepo

The aim of the application and PyTeal contract is to deposit Algo or Algorant Standard Assets in a single Transaction.

User compiles a deposit app call transaction and sets the [rekeyTo](https://developer.algorand.org/docs/get-details/transactions/transactions/#common-fields-header-and-type) field to the address of the contract.

This is the building block for more complex applications on Algorand and its ecosystem.

Submission for https://gitcoin.co/issue/c3protocol/hackalgo/1/100028569

### Contract Args

The contract takes 2 args.

The first arg is the type fo transaction: deposit or asa_deposit.
The second arg is the amount deposited.
## Installation 

Required instalation of Python3 and NPM.

### Python Environment

```bash
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

One line if virtualenv is installed:

```bash
virtualenv venv && source venv/bin/activate && pip install -r requirements.txt
```

To convert Pyteal to teal contract:
```bash
python3 /contracts/contract.py
```

### NPM

To install packages:
```bash
npm i
```

## Run the Deposit App

First add Mnemonic passphrase to ```.env```.
Next go to the [testnet dispenser](https://dispenser.testnet.aws.algodev.network/) to obtain Algo. Create an asset using ```createasset.py``` or obtain one from a faucet and enter its id in ```config.js```.

To illustrate the app run:

```bash
npm start
```

Such that

![img](https://i.imgur.com/qwBnpYV.png)

Illustration of the working app on AlgoExplorer:

https://testnet.algoexplorer.io/application/85314426

## Overview of the .js files

```asa_deposit.js``` deposits asa asset

```config.js``` contains the user instance and id of the asset to transfer

```deploy.js``` deploys contract ie approval and clear state teal files

```deposit.js``` deposits Algo

```index.js``` runs deploy, deposit and asa_deposit 

```utils.js``` contains instance of Algorand Client, submitTransaction function to sign, send and wait for transaction confirmation

### Further Resources

[Pyteal](https://pyteal.readthedocs.io/en/stable/index.html)