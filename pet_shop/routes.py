#!/usr/bin/env python3

from flask import render_template, redirect, url_for  # 1
from flask import request, session  # 1
from pet_shop import app, db  # 1

@app.route('/')  # 1
def PStore():  # 1
    """simple return string"""
    return"Welcom to my new pet store"  # 1
