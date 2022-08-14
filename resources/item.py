from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="This field cannot be left blank!")
    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)

        try:
            if item:
                return item.json(), 200
            return {"message": "Item not found"}, 404

        except Exception as e:
            return {"message": "An error while fetch the item", "ex": str(e)}, 500

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name \'{name}\' already exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
            return item.json(), 201

        except Exception as e:
            return {"message": "An error occurred inserting the item", "ex": str(e)}, 500

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        
        try:
            if item:
                item.delete_from_db()
                return {"message": "Item deleted"}, 200
    
            return {'message': 'Item not found'}, 404

        except Exception as e:
            return {"message": "An error occurred while deleting the item", "ex": str(e)}, 500

    def put(self, name):

        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
       
        if item is None:
            try:
                item = ItemModel(name, **data)

            except Exception as e:
                return {"message": "An error occurred while inserting the item", "ex": str(e)}, 500
        else:
            try:
                item.price = data["price"]

            except Exception as e:
                return {"message": "An error occurred while updating the item", "ex": str(e)}, 500
        
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):    
        return {"items": [item.json() for item in ItemModel.query.all()]}
