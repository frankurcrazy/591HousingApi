#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""591 parsing service
"""

import re

from flask import Flask, jsonify

from py591.parse import get_591_info

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.config["JSON_AS_ASCII"] = True
pattern = re.compile(r"^https://rent.591.com.tw/rent-detail-\d+.html$")


@app.route("/591/<path:url>")
def get_info(url):
    """Get rental information from 591 link"""
    if not pattern.match(url):
        return jsonify(
            {
                "status": "error",
                "message": "Not supported",
            }
        )

    try:
        info = get_591_info(url)

        result = {
            "status": "success",
            "result": info,
        }

    except Exception as e:
        result = {
            "status": "error",
            "message": repr(e),
        }

    return jsonify(result)


if __name__ == "__main__":
    app.run()
