# Poly-visor

A centralized supervisor web-based UI using SvelteKit and FLASK

* Lightweight plugin
* Processes status always up to date
* Reactivity through asynchronous actions
* Works on supervisord
* Observe the resources of comuter through charts visualized using ChartJS
* Allow user to create and edit configuration file via web page (permission required)

## Installation

This version has only been tested on Linux OS.

To install polyvisor. The following steps need to be followed exactly.

### Requirements
Polyvisor needs some packages to run, install by ```pip```:
```bash
pip install -r requirements.txt
```

### Web server
Clone the repository from git
```bash
git clone https://github.com/poly-laboratory/poly-visor.git
cd poly-visor
```
Install npm dependencies for front-end and build to production
```bash
npm install
npm run build
```

Install poly-visor via pip
```bash
pip install .
```

Add the following line to supervisord config file
```ini
[rpcinterface:polyvisor]
supervisor.rpcinterface_factory = polyvisor.rpc:make_rpc_interface
bind=5000
access_point=auto
```
```access_point``` is optional, you can remove it if you don't want to access the web dashboard from LAN.
You can specify access_point on an IP address or set to ```auto```, the program will automatically search for IP and get that value, if there is no data, they will run on ```localhost```

Run supervisord along with polyvisor via supervisord.conf
```bash
supervisord -c /route/to/conf/supervisord.conf
```

To run multiple supervisord instances, first create a polyvisor.ini file to store all the urls of each supervisord instance (which is the "serverurl" in the "[supervisorctl]" section)
```ini
[supervisor:<name of the first supervisord instance>]
url=<url of the first supervisord instance>

[supervisor:<name of the second supervisord instance>]
url=<url of the second supervisord instance>
```
And then run the supervisord instances sequentially with the following command
```bash
supervisord -c /route/to/conf/first_supervisord_instance.conf
supervisord -c /route/to/conf/second_supervisord_instance.conf
``` 
After that run the polyvisor rpc interface via supervisord

Here is the example

polyvisor.ini:
```ini
[supervisor:lid001]
url=localhost:9011


[supervisor:lid002]
url=localhost:9021


[global]
name=Test
```

lid001.conf:
```ini
[inet_http_server]
port=:9011

[supervisord]
logfile_backups=10
logfile_maxbytes=1MB
pidfile=/tmp/supervisor_lid001.pid
identifier=lid001

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=http://localhost:9011

[include]
files = /etc/supervisor/conf.d/*.ini; change your process directory accordingly
```

lid002.conf:
```ini
[inet_http_server]
port=:9021

[supervisord]
logfile_backups=10
logfile_maxbytes=1MB
pidfile=/tmp/supervisor_lid002.pid
identifier=lid002

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=http://localhost:9021

[include]
files = /etc/supervisor/conf2.d/*.ini; change your process directory accordingly
```


# Development

## Development mode
In development mode. The rpcinterface must not be included in the configuration file

Run the front-end in development mode:
```bash
npm run dev
```

The back-end can be run with the following command
```bash
flask run
```

## Build and install
```bash
# Build the front-end via npm
npm run build

# Re-install your built files
pip install .
```
