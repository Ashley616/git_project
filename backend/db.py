from init import db
from app import app
import sys
from mysqldb import Recipe, User
import csv

if __name__ == '__main__':
    if sys.argv[1] == '--create':
        db.create_all(app=app)
        # df = pd.read_csv('recipes.csv', nrows=1000)
        app_context = app.app_context()
        app_context.push()
        with open('smaller_db_new.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            tag = 0
            if tag < 1000:
                for i in reader:
                    if i[1] == 'id':
                        pass
                    else:
                        recipe = Recipe(Rid=i[1], recipeName=i[2], description=i[3], ingredients=i[4],
                                        ingredientWeight=i[5], steps=i[8], type=i[10], uploader=1)
                        db.session.add(recipe)
                        db.session.commit()
                tag += 1
        user = User(id=1, name='Admin', password='456', email='123@hotmail.com', role='contributor')
        db.session.add(user)
        db.session.commit()
    elif sys.argv[1] == '--drop':
        db.drop_all(app=app)
    else:
        print('Operations on database --[create|drop]')
