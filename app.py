#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from parse import get_591_info

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

@app.route('/591/<path:url>')
def get_info(url):
    try:
        info = get_591_info(url)

        result = {
            'status': 'success',
            'result': info,
        }

    except Exception as e:
        result = {
            'status': 'error',
            'message': repr(e),
        }

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

