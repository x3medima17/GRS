from websocket import create_connection
import random
import time


def slice(lst,size):
	result = []
	lst = [str(x) for x in lst]
	for i in xrange(len(lst)/size):
		curr = lst[size*i:size*i+size]
		result.append(curr)
	return result

ws = create_connection("ws://localhost:9090/ws")


axes = ['heading','pitch','roll']
fingers = ['wrist','thumb','index','middle','ring','pinky']

epsilon = 2
lst = [int(random.uniform(0,100)) for x in range(18)]

total = 0
neg = 0

while True:
	# print random.uniform(-epsilon,epsilon)
	total += 1
	if random.uniform(-epsilon,epsilon) < 0:
		neg += 1
	# print neg*1.0 / total
	lst = [int(x+random.uniform(-epsilon,epsilon+2)) for x in lst]
	lst = [int(random.uniform(0,100)) if x<0 or x> 100 else x for x in lst]
	message =   ";".join([" ".join(x) for x in slice(lst,3)])
	ws.send(message)
	print message
	time.sleep(0.1)

ws.close()