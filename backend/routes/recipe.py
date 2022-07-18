from mysqldb import *
from flask import Blueprint, json, request, render_template, session, flash, jsonify
from flask_jwt_extended import (create_access_token, current_user, jwt_required, JWTManager, create_refresh_token)
from mysqldb import User, db, Recipe
from datetime import timedelta


JWT_EXPIRE_TIME = timedelta(minutes=30)
bp = Blueprint('recipe', __name__, url_defaults='')


@bp.route('/create', methods=['POST'])
def create():
    recipeName = request.json['recipename']
    if recipeName == '':
        return jsonify("recipename is required."), 400

    description = request.json['description']

    ingredients = request.json['ingredients']
    if ingredients == '':
        return jsonify("ingredients is required."), 400

    ingredientWeight = request.json['ingredientWeight']
    if ingredientWeight == '':
        return jsonify("ingredientWeight is required."), 400

    steps = request.json['steps']
    if steps == '':
        return jsonify("steps is required."), 400

    type = request.json['type']

    uploader = request.json['userId']

    recipe = Recipe()
    recipe.recipeName = recipeName
    recipe.description = description
    recipe.ingredients = ingredients
    recipe.ingredientWeight = ingredientWeight
    recipe.steps = steps
    recipe.type = type
    recipe.uploader = uploader
    db.session.add(recipe)
    db.session.commit()
    recipe = {"id": recipe.Rid, "name": recipe.recipeName, "description": recipe.description,
              "ingredients": recipe.ingredients, "ingredientsWeight": recipe.ingredientWeight,
              "steps": recipe.steps,"type": recipe.type}
    return jsonify(recipe), 200


@bp.route('/check', methods=['POST'])
def check():
    user = request.json['userId']
    res = db.session.query(Recipe).filter_by(uploader=user).all()
    recipe = {}
    num = 0
    if res:
        for i in res:
            recipe[num] = {"id": i.Rid, "name": i.recipeName, "description": i.description,
                           "ingredients": i.ingredients, "ingredientsWeight": i.ingredientWeight,
                           "steps": i.steps, "type": i.type}
            num += 1
    return jsonify(recipe), 200


@bp.route('/edit', methods=['POST'])
def edit():
    recipeId = request.json['Rid']
    recipeName = request.json['recipename']
    if recipeName == '':
        return jsonify("recipename is required."), 400

    description = request.json['description']

    ingredients = request.json['ingredients']
    if ingredients == '':
        return jsonify("ingredients is required."), 400

    ingredientWeight = request.json['ingredientWeight']
    if ingredientWeight == '':
        return jsonify("ingredientWeight is required."), 400

    steps = request.json['steps']
    if steps == '':
        return jsonify("steps is required."), 400

    type = request.json['type']

    recipe = db.session.query(Recipe).filter_by(Rid=recipeId).first()
    recipe.recipeName = recipeName
    recipe.description = description
    recipe.ingredients = ingredients
    recipe.ingredientWeight = ingredientWeight
    recipe.steps = steps
    recipe.type = type
    db.session.commit()

    recipe = {"id": recipe.Rid, "name": recipe.recipeName, "description": recipe.description,
              "ingredients": recipe.ingredients, "ingredientsWeight": recipe.ingredientWeight,
              "steps": recipe.steps, "type": recipe.type}

    return jsonify(recipe), 200


@bp.route('/delete', methods=['POST'])
def delete():
    recipeId = request.json['Rid']
    recipe = db.session.query(Recipe).filter_by(Rid=recipeId).first()
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify("delete success!"), 200
    else:
        return jsonify("No such recipe!"), 401



