argument=$1
argument2=$2
start="start"

if [ "$argument" = start ]; then
	echo "Starting system"
	nohup python backend/main.py & 1>/dev/null 2>&1
	nohup python frontend/main.py & 1>/dev/null 2>&1
fi

if [ "$argument2" = full ]; then
	sleep 1
	nohup python backend/client.py & 1>/dev/null 2>&1
fi

if [ "$argument" = stop ]; then
	echo "Stop system"
	killall python 1>/dev/null 2>&1
fi


