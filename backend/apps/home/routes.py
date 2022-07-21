# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/index')
#@login_required
def index():

    return render_template('home/index.html', segment='index')


@blueprint.route('/<template>')
#@login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


@blueprint.route('/verify_doping', methods  = ["POST", "GET"])
def verify_doping():

    if request.method == "POST":
        #hormone_1 = request.form['h1']
        specific_gravity = request.form['specific_gravity']
        in_comp = request.form['in_comp']
        adiol = request.form['adiol']
        andro = request.form['andro']
        etio = request.form['etio']
        epito = request.form['epito']
        testes = request.form['testes']
        male = request.form['male']
        athlete_id = request.form['athlete_id']

        print("hormone_1", hormone_1)

        # logic for processing for doping and modeling
        generated_message = "Based on our analysis we conclude that the provided sample do not corrospond to any levels of doping."

        return render_template('home/page-blank.html', generated_message = generated_message)


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
