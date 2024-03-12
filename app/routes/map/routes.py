# -*- coding: utf-8 -*-
from flask import redirect, url_for, render_template, abort, request, current_app
from app import db, models
import app.routes.map.funcs as funcs
import json
import re
import math
from datetime import date
from requests import HTTPError
from app.routes.map import bp

# ======== Routing =========================================================== #

# -------- Home page ---------------------------------------------------------- #


@bp.route("/explore/")
@bp.route("/")
@bp.route("/map/", methods=['GET', 'POST'])
def map():
    q_address = request.args.get('loc')
    q_radius = request.args.get('rad')
    q_skill = request.args.get('ski')
    q_gender = request.args.get('gen')
    q_min_age = request.args.get('min')
    q_max_age = request.args.get('max')
    q_include_erc360s = True # Remember to add on/off tick front end

    q_strings = {"selected_address": q_address, "selected_radius": q_radius, "selected_skill": q_skill, "selected_gender": q_gender, "selected_min_age": q_min_age, "selected_max_age": q_max_age}

    if request.method == 'POST':

        address = request.form.get("location")
        skill = request.form.get("skill")
        radius = request.form.get("radius")
        gender = request.form.get("gender")
        min_age = request.form.get("min_age")
        max_age = request.form.get("max_age")

        location = funcs.geocode(address)

        if not location:
            return json.dumps({'status': 'Non-valid location', 'box_id': 'location-field'})

        try:

            radius = float(radius)

        except ValueError:
            return json.dumps({'status': 'Non-valid radius', 'box_id': 'options-button'})

        url = f'/map?loc={address}&rad={radius}'

        if skill:
            if skill in current_app.config["AVAILABLE_SKILLS"]:
                url += f'&ski={skill}'
        if gender:
            if gender in current_app.config["AVAILABLE_GENDERS"]:
                url += f'&gen={gender}'
        if min_age:
            url += f'&min={min_age}'
        if max_age:
            url += f'&max={max_age}'

        query = models.User.get_explore_query(latitude=location.latitude, longitude=location.longitude, radius=radius, skill=skill, gender=gender, min_age=min_age, max_age=max_age)
        
        if q_include_erc360s:
            erc360_query = models.ERC360.get_explore_query(latitude=location.latitude, longitude=location.longitude, radius=radius)
            erc360s = erc360_query.all()
        else:
            erc360s = []

        users = query.all()

        loc = {"lat": location.latitude, "lng": location.longitude, "zoom": funcs.get_zoom_from_rad(radius)}
        users_info = [{"username": u.username, "photo": u.photo.src, "name": u.name if u.name else u.username, "lat": u.latitude, "lng": u.longitude} for u in users]
        erc360s_info = [{"address": e.address, "photo": e.photo.src, "name": e.name, "symbol": e.symbol, "lat": e.latitude, "lng": e.longitude} for e in erc360s]
        return json.dumps({'status': 'Successfully explored', 'url': url, 'users_info': users_info, 'erc360s_info':erc360s_info, 'loc': loc})

    return render_template("map.html", available_skills=current_app.config["AVAILABLE_SKILLS"], available_genders=current_app.config["AVAILABLE_GENDERS"], background=False, footer=False, exonavbar=True, ** q_strings)


@ bp.route("/about/", methods=['GET'])
def about():
    return render_template("about.html", background=True, size="medium", footer=True, navbar=True)


@ bp.route("/fiskefrikadeller/", methods=['GET'])
def fiskefrikadeller():
    return render_template("fiskefrikadeller.html", testvar="yes", background=True, size="medium", footer=True, navbar=True)


@ bp.route("/help/", methods=['GET'])
def help():
    return render_template("help.html", background=True, size="medium", footer=True, navbar=True)


@ bp.route("/settings/", methods=['GET'])
def settings():
    return render_template("settings.html", background=True, size="medium", footer=True, navbar=True)
