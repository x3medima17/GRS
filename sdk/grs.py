import pymongo
import fx
import os
from os.path import expanduser
from pprint import pprint
from websocket import create_connection
import math as Math
import redis
import sys
from subprocess import Popen, PIPE
mem = redis.StrictRedis(host='localhost', port=6379, db=0)


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
			trained = False
			)
		data["class"] = self.db.gestures.find().count()+1
		self.db.gestures.insert(data)
		return fx.gen_result(0,"Gesture added")

	def get_raw_data(self):
		data = mem.get('raw_data')
		return data

	def point(self,distance):
		data = self.get_raw_data()
		if not data:
			return 
		data  = data.replace(";"," ").split(" ")
		# print data
		quaternion = [int(x) for x in data[-4:]]
		q0 = quaternion[0]
		q1 = quaternion[1]
		q2 = quaternion[2]
		q3 = quaternion[3]
		q = quaternion
		heading = Math.atan2(2*q1*q2 - 2*q0*q3, 2*(q0*q0) + 2*(q1*q1) - 1)
		try:
			pitch = -Math.asin(2*q1*q3 + 2*q0*q2)
		except:
			pitch = 0.6
		roll = Math.atan2(2*q2*q3 - 2*q0*q1, 2*(q0*q0) + 2*(q3*q3) - 1)
		
		x,y,z = 0,0,-1
		qx = q[0];
		qy = q[1];
		qz = q[2];
		qw = q[3];

		ix =  qw * x + qy * z - qz * y;
		iy =  qw * y + qz * x - qx * z;
		iz =  qw * z + qx * y - qy * x;
		iw = - qx * x - qy * y - qz * z;

		x = ix * qw + iw * - qx + iy * - qz - iz * - qy;
		y = iy * qw + iw * - qy + iz * - qx - ix * - qz;
		z = iz * qw + iw * - qz + ix * - qy - iy * - qx;

		x,y,z = x*distance,y*distance,z*distance
		cmd = "xdotool mousemove %s %s" % (x,y)
		p = Popen(cmd.split(' '),stdout=PIPE)
		out = p.communicate()
		s = " ".join([str(x),str(y),str(z)])
		sys.stdout.write("\r%s" % s) 
		sys.stdout.flush()


	def prepare_training_set(self):
		K = self.db.gestures.count()
		data = list(self.db.gestures.find())
		f = open('nn/dataNN.dat','w')
		for item in data:
			for tr in item["training_data"]:
				f.write(tr+" "+str(item["class"])+"\n")


	def train(self):
		os.chdir("nn")
		cmd = "octave train.m".split()
		proc = Popen(cmd,stdout=PIPE)
		out,err = proc.communicate()
		os.chdir("../")
		self.db.gestures.update({},{"$set":{"trained":True}},multi=True)

	def predict(self):
		os.chdir("nn")
		data = self.get_raw_data()
		if not data:
			print "No data"
			return 
		data  = data.replace(";"," ").split(" ")
		# print data
		data = [x for x in data[-4:]]
		f = open('X.txt',"w")
		f.write(" ".join(data))
		f.close()
		cmd = "octave predict_direct.m".split()
		proc = Popen(cmd,stdout=PIPE)
		out,err = proc.communicate()
		os.chdir("../")
		result = open("nn/result.dat","r").readlines()
		# print result
		return int(result[-3].replace('\n',''))

	def get_gesture(self,id):
		return self.db.gestures.find_one({"class":id})["name"]



#os.chdir(aPath)
print os.getcwd()


if __name__ == "__main__":
	import time
	grs = GRS()
	# grs.prepare_training_set()
	# grs.train()
	while True:
		p = grs.predict()
		print p,
		gesture = grs.db.gestures.find_one({"class":p})
		print gesture['name']
		# time.sleep(0.3)