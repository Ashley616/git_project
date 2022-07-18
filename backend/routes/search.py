from mysqldb import *
from flask import Blueprint, json, request, render_template, session, flash, jsonify
from flask_jwt_extended import (create_access_token, current_user, jwt_required, JWTManager, create_refresh_token)
from mysqldb import User, db, Recipe
from datetime import timedelta


JWT_EXPIRE_TIME = timedelta(minutes=30)
bp = Blueprint('search', __name__, url_defaults='')


@bp.route('/type', methods=['POST'])
def search_by_type():
    types = request.json['type']
    res = db.session.query(Recipe).filter(Recipe.type.like(f'%{types}%')).all()
    recipe = {}
    num = 0
    if res:
        for i in res:
            uploader = db.session.query(User).filter_by(id=i.uploader).first()
            recipe[num] = {"id": i.Rid, "name": i.recipeName, "description": i.description,
                           "ingredients": i.ingredients, "ingredientsWeight": i.ingredientWeight,
                           "steps": i.steps, "type": i.type, "uploader": uploader.name}
            num += 1
        return jsonify(recipe), 200
    else:
        return jsonify("No such type!"), 401


@bp.route('/follow', methods=['POST'])
def follow():
    uploader = request.json['uploader']   # contributor name
    contributor = db.session.query(User).filter_by(name=uploader).first()
    userid = request.json['userId']
    res = db.session.query(User).filter_by(id=userid).first()
    if res.follow is None:
        res.follow = contributor.id
        db.session.commit()
        return jsonify("follow success"), 200
    elif str(contributor.id) not in res.follow:
        res.follow = res.follow + ',' + str(contributor.id)
        db.session.commit()
        return jsonify("follow success"), 200
    else:
        return jsonify("you have already follow him."), 401
