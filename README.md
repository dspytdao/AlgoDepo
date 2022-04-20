# AlgoDepo

The aim of the following contract is to

This is the building block for more complex applications on Algorand and its ecosystem.

Submission for https://gitcoin.co/issue/c3protocol/hackalgo/1/100028569
## Installation 

### Python Environement

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

### Contract Args

takes 2 args in case of Algo deposit. 
type of the tx
amount

for instance:

app_args = [b"deposit", 1]

### SandBox (testing Environment)


### Further Resources

[Pyteal](https://pyteal.readthedocs.io/en/stable/index.html)