## Diana - A Discord Bot

A discord bot written in Python.

### INSTALL

Clone the repo.

Ensure you have python 3.6 installed:

##### Linux

```sh
$ wget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz

$ tar xzf Python-3.6.1.tgz

$ cd Python-3.6.1
$ ./configure
$ make altinstall
```

##### Windows

Download and install:
https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe


#### Run INSTALL script

```sh
$ cd ~/Diana
$ python3.6 install.py
```

### Configure

Make any changes necessary to config files, most importantly the API tokens required for the bot.
```
# Discord bot config
./diana.conf

# Flask app config.
./config/__init__.py
```


## Run

```sh
$ python3.6 run.py
```
