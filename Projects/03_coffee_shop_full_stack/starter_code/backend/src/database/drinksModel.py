from src.database.models import db, Drink
import json
import copy


def getDrinks():
    results = db.session.query(Drink).all()
    drinks = []
    for drink in results:
        drinks.append(drink.short())
    return drinks


def getDrinksDetails():
    results = db.session.query(Drink).all()
    drinks = []
    for drink in results:
        drinks.append(drink.long())
    return drinks


def insertDrink(newDrink):
    response = {"success": True}

    try:
        """
        we need to put the recipe into array
        """
        if not isinstance(newDrink['recipe'], list): # in case that we have only on element in the recipe
            newDrink['recipe'] = [newDrink['recipe']]
        """
            is json able to ignore multiple [] ??
        """
        # check if the new drink violating unique constrains [title exist
        # before]
        oldDrink = db.session.query(Drink).filter(
            Drink.title == newDrink['title']).one_or_none()
        if oldDrink is not None:
            response['success'] = False
            response['error'] = "drink title already exist"
            response['status_code'] = 409
        else:
            drinkObj = Drink(
                title=newDrink['title'],
                recipe=json.dumps(
                    newDrink['recipe']))
            drinkObj.insert()
            response['drink'] = drinkObj

    except Exception as err:
        print("failure in inserting new drink ", err)

        response['success'] = False
        response['error'] = "internal server error please call support"
        response['status_code'] = 500

        db.session.rollback()
        drinkObj = None

    finally:
        db.session.close()

    return response


def patchDrink(id, data):
    title = data.get('title', "");
    recipe = data.get('recipe', "");
    if type(recipe) !=list:  # in case that we have only on element in the recipe
        recipe = [recipe];

    response = {"drink": None, "success": True, "status_code": 200}

    try:
        drinkObj = db.session.query(Drink).filter(Drink.id == id).one_or_none()
        if drinkObj is None:
            response['success'] = False
            response['status_code'] = 404
        else:
            drinkObj.title = title
            drinkObj.recipe = json.dumps(recipe);
            drinkObj.update()
            response["drink"] = drinkObj

    except Exception as err:
        print("failure in patchDrinkn ", err)
        response['success'] = False
        response['status_code'] = 500
        db.session.rollback()

    finally:
        db.session.close()
    return response


def deleteDrink(id):
    response = {"success": True, "status_code": 200}

    try:
        drinkObj = db.session.query(Drink).filter(Drink.id == id).one_or_none()
        if drinkObj is None:
            response['success'] = False
            response['status_code'] = 404
        else:
            drinkObj.delete()

    except Exception as err:
        print("failure in deleteDrink ", err)
        response['success'] = False
        response['status_code'] = 500
        db.session.rollback()

    finally:
        db.session.close()

    return response
