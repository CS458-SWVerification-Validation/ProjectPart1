from flask import request, jsonify, flash, redirect, url_for, render_template, render_template_string
from flask_login import login_user, login_required, logout_user, current_user

from app.survey import bp
from app.extensions import db
from app.models.user import User, OnlineUser
from app.models.survey import Survey
from app.survey.forms import SurveyForm

final_uri = "myapp://home"

@bp.route("/submit/<user_id>", methods=["POST"])
def submit_survey(user_id):
    user = User.query.filter(user_id).first_or_404()
    if user: 
        survey = Survey(
            user_id=user_id,
            name=request.get('name'),
            surname=request.get('surname'),
            birth_date=request.get('birthDate'),  # convert string to date if needed
            education_level=request.get('educationLevel'),
            city=request.get('city'),
            gender=request.get('gender'),
            ai_models=request.get('aiModels'),
            defects=request.get('defects'),
            use_case=request.get('useCase')
        )
        db.session.add(survey)
        db.session.commit()
        return jsonify({'message': 'Survey submitted successfully'}), 200
    else:
        return jsonify({'message': 'User does not exist'}), 200