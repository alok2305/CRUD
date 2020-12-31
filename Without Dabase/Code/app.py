from flask import  Flask ,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import  JWT ,jwt_required
from security import authenticate,identity
app=Flask(__name__)
api=Api(app)
app.secret_key="flask"

jwt=JWT(app,authenticate,identity)
items=[]

class Item(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help="This field cannot be left blank")
    
    @jwt_required()
    def get(self,name):
        item=next(filter(lambda x : x['name']==name , items),None)
        return {"item": item} , 200 if item else 404
    def post(self,name):
        if next(filter(lambda x : x['name']==name , items),None):
            return {'message' : 'An item with name ' + name +  ' already exist'} ,400
        data=Item.parser.parse_args()
        item={'name':name , 'price': data['price']}
        items.append(item)
        return item ,201
    def delete(self,name):
        global items
        items=list(filter(lambda x : x['name']!=name ,items))
        return {'message': 'Item Deleted'}
    def put(self,name):
        data=Item.parser.parse_args()
        item=next(filter(lambda x : x['name']==name , items),None)
        if item is None:
            item={'name':name,'price': data['price']}
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        return {'items': items}

api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
if __name__ == "__main__":
    app.run(debug=True)

