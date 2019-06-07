from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every items needs a store id"
    )


    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return { "message":"Item not found" }

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {
                "message":f"item with name {name} already exists"
            }, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)
        try:
             item.save_to_db()
        except:
            return {"message":"An error occured"}, 500
        return item.json(), 200


    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {"message":"item deleted"}

    def put(self, name):
        item = ItemModel.find_by_name(name)

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        if item is None:
            try:
               item = ItemModel(name, **data)
            except:
                return {"message":"An error occured"}, 500
        else:
                item.price= data['price']
        item.save_to_db()
        return item.json(), 200


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all() ]}