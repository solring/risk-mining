if [ "$#" -lt "2" ]; then
	echo "usage: run.sh [input dir] [output dir]"
	exit 0
fi

java -jar CKIPClient.jar ckipsocket.propeties $1 $2
