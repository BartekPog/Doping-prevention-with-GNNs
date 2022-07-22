# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import sys, os


from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound

from apps.home import blueprint

from prediction.prediction import Predictor



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
        sample_dict = {
            'specific_gravity':  float(request.form['specific_gravity']),
            'in_competition': bool(request.form['in_comp'] in {'1', "True", True, 'true', 'male', 'Yes', 'yes'}),
            'adiol': float(request.form['adiol']),
            'bdiol':  float(request.form['bdiol']),
            'androsterone':  float(request.form['andro']),
            'etiocholanolone':  float(request.form['etio']),
            'epitestosterone':  float(request.form['epito']),
            'testosterone':  float(request.form['testes']),
            'is_male': bool(request.form['male'] in {'1', "True", True, 'true', 'male', 'Yes', 'yes'}),
            'athlete_id': int(request.form['athlete_id']),
        }

        predictor = Predictor()
        anomaly_score = predictor.predict_sample(sample_dict)

        max_score = max(predictor.predictions)

        percentage_score = 100*anomaly_score / max_score

        generated_message = f"Based on comparsion of anamoly scores of this urine sample with other athletes we can say with {percentage_score:.2f}% confidence that it is swapped "

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
