import grs

obj = grs.GRS()

while True:
	p = obj.predict()
	print obj.get_gesture(p)