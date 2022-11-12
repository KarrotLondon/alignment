#!/bin/bash

poetry run gunicorn -w 2 --threads 2 --bind 0.0.0.0:$PORT 'src:create_app()'

exec $@