from flask import Flask, request
from flask_restful import Resource, Api, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

api = Api(app)


# configuration of datatbase

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

# create model 

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __repr__(self):
        return self.name


# here we are going to serialize 

taskfields = {
    'id': fields.Integer,
    'name': fields.String
}


fakeDatabase = {
    1: {'name': "Clean Car"},
    2: {'name': "write blog"},
    3: {'name': "Start Stream"},
}
@app.route('/create')
def create():
    db.create_all()
    return 'All tables created'


class Items(Resource):
    @marshal_with(taskfields)
    def get(self):
        tasks = Task.query.all()
        return tasks
    @marshal_with(taskfields)
    def post(self):
        data = request.json
        task = Task(name=data['name'])
        db.session.add(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks


class Item(Resource):
    @marshal_with(taskfields)
    def get(self, pk):
        task = Task.query.filter_by(id=pk).first()
        return task
    @marshal_with(taskfields)
    def put(self, pk):
        data = request.json
        task = Task.query.filter_by(id=pk).first()
        task.name = data['name']
        db.session.commit()
 
        return task
    @marshal_with(taskfields)
    def delete(self, pk):
        task = Task.query.filter_by(id=pk).first()
        db.session.delete(task)
        db.session.commit()
        tasks = Task.query.all()
        return tasks

# here we were using fake database

# class Items(Resource):
#     def get(self):
#         return fakeDatabase
#     def post(self):
#         data = request.json
#         itemId = len(fakeDatabase.keys()) + 1
#         fakeDatabase[itemId] = {'name': data['name']}
#         return fakeDatabase


# class Item(Resource):
#     def get(self, pk):
#         return fakeDatabase[pk]
#     def put(self, pk):
#         data = request.json
#         fakeDatabase[pk]['name'] = data['name']
 
#         return fakeDatabase
#     def delete(self, pk):
#         del fakeDatabase[pk]
#         return fakeDatabase

api.add_resource(Items, '/')
api.add_resource(Item, '/<int:pk>')

if __name__ == "__main__":
    app.run(debug=True)