#!/usr/bin/env python3

from flask import render_template, redirect, url_for
from flask import request, session
from pet_shop import app, db

@app.route('/')
def PStore():
    return"Welcom to my new pet store"
