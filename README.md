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
Polyvisor needs these packages to run, install by:
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
supervisor.rpcinterface_factory = polyvisor.rpc:make_rpc_interfacce
bind=5000
```

Run supervisord along with polyvisor via supervisord.conf
```bash
supervisord -c /route/to/conf/supervisord.conf
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
