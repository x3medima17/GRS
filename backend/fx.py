import json
import kdtree
import pymongo
import math as Math
conn = pymongo.MongoClient()

db = conn.grs

magn_to_gyro_data = list(db.magn.find())

def gen_result(status,message,data=None):
	result = dict(
		status = status,
		message = message,
		data = data
		)
	return json.dumps(result)

def magn_to_gyro(x,y,z,tree):
	x,y,z = tree.search_nn((x,y,z))[0].data
	data = db.magn.find_one(dict(
		x = float(x),
		y = float(y),
		z= float(z),
		))
	return data


def build_tree(data):
	tree = kdtree.create(dimensions=3)
	for item in data:
		curr = item
		node = [curr['x'],curr['y'],curr['z']]
		tree.add(node)
	tree = tree.rebalance()
	return tree


