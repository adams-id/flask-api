from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

#Setting up the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  views = db.Column(db.Integer, nullable=False)
  likes = db.Column(db.Integer, nullable=False)

  def __repr__(self):
    return f"Video(name={name}, views={views}, likes = {likes})"

#Run this line of code on your first start then coomment it out.This setups up the database initially and removing it prevents us from overwriting the db
#db.create_all()

#This is to be able to set parameters to be sent as payload when the user is making a request
video_post_args = reqparse.RequestParser()
video_post_args.add_argument("name", type=str, help="Name of the video is required", required=True)
video_post_args.add_argument("views", type=int, help="Views of the video is required", required=True)
video_post_args.add_argument("likes", type=int, help="Likes on the video is required", required=True)


video_update_agrs = reqparse.RequestParser()
video_update_agrs.add_argument("name", type=str, help="Invalid name")
video_update_agrs.add_argument("views", type=int, help="Invalid views")
video_update_agrs.add_argument("likes", type=int, help="Invalid likes")

resource_fields = {
  "id": fields.Integer,
  "name": fields.String,
  "views": fields.Integer,
  "likes": fields.Integer
}

class Video(Resource):
  @marshal_with(resource_fields)
  def get(self, video_id):
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, message="Video id is not valid...")
    return result

  @marshal_with(resource_fields)
  def post(self, video_id):
    #args is the payload gotten from the request
    args = video_post_args.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first()
    if result:
      abort(409, message="Video with that id already exists...")
    video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
    db.session.add(video)
    db.session.commit()
    return video, 201

  @marshal_with(resource_fields)
  def patch(self, video_id):
    args = video_update_agrs.parse_args()
    result = VideoModel.query.filter_by(id=video_id).first()
    if not result:
      abort(404, message="Video doesn't exist, cannot update...")

    if args["name"]:
      result.name = args["name"]
    if args["views"]:
      result.views = args["views"]
    if args["likes"]:
      result.likes = args["likes"]

    db.session.commit()

    return result

#Adding the resource where first parameter is the resource and second parameter is the url user calls
api.add_resource(Video, "/video/<int:video_id>")

#This line of code runs the application and puts it in debug mode. Remove debug from true if you are running in prod
if __name__ == "__main__":
  app.run(debug=True)

