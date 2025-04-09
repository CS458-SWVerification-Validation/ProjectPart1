from flask import request, jsonify, flash, redirect, url_for, render_template, render_template_string
from flask_login import login_user, login_required, logout_user, current_user

from app.survey import bp
from app.extensions import db
from app.models.user import User, OnlineUser
from app.survey.forms import SurveyForm

final_uri = "myapp://home"

@bp.route("/submit", methods=["POST"])
def submit_survey():
    return jsonify("Succeed"), 200