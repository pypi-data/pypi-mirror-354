# sopel-http
[![PyPi Version](https://img.shields.io/pypi/v/sopel-http.svg)](https://pypi.org/project/sopel-http/)

Interact with your [Sopel](https://github.com/sopel-irc/sopel) bot over HTTP

## Setup
Only developers should need to install this package directly, but they can do
so with a simple `pip install sopel-http`.

## Configuration
You can change which IP addresses and ports `sopel-http` binds to in your Sopel
configuration. For example, to bind to port 8080 on all IPs (including public!):
```ini
[http]
bind = "[::]:8080"
```
By default it listens on 127.0.0.1 and ::1 (localhost), port 8094.

## Usage
See the example plugin,
[sopel-http-example](https://github.com/half-duplex/sopel-http-example).

Once you've created and registered the flask
[Blueprint](https://flask.palletsprojects.com/en/2.1.x/blueprints/)
as shown in the example, you can use it more or less like any other flask
application.
