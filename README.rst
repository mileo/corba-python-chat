==========
Corba Chat
==========

Summary:

* Flask Microservice
* Chat application
* Corba protocol

Install Server
==============

- Fork this repository
- Clone this repository
- Dependencies
 * python-omniorb
 * omniidl
 * omniidl-python
 * omniorb
 * omniorb-nameserver

On ubuntu 16.04:
> sudo apt-get install python-omniorb omniidl omniidl-python omniorb omniorb-nameserver


```
virtualenv -p python3.5 env --system-site-packages
source env/bin/activate exit
pip install -r requirements.txt
```

Using
-----

```
python app.py
```
