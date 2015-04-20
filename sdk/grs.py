import pymongo
import fx
import os
from os.path import expanduser
from pprint import pprint

home = expanduser("~")
path = "%s/grs/sdk" % home

os.chdir(path)
class GRS(object):
	def __init__(self,db="grs"):
		self.conn = pymongo.MongoClient()
		self.db = self.conn[db]

	def set_db(self,db):
		self.db = self.conn[db]

	def get_gestures(self):
		data = list(self.db.gestures.find())
		pprint(data)

	def get_gesture(self,name):
		return self.db.gestures.find_one({"name":name})

	def add_gesture(self,name,training_data):
		if(self.get_gesture(name)):
			return fx.gen_result(1,"Gesture already exists")

		data = dict(
			name = name,
			training_data = training_data,
			)
		data["class"] = self.db.gestures.find().count()
		self.db.gestures.insert(data)
		return fx.gen_result(0,"Gesture added")

#os.chdir(aPath)
print os.getcwd()


if __name__ == "__main__":
	grs = GRS()
	name = "point2"
	training_data = []
	print grs.add_gesture(name,training_data)