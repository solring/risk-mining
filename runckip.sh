if [ "$#" -lt "2" ]; then
	echo "usage: run.sh [input dir] [output dir]"
	exit 0
fi

indir=$1
outdir=$2

for f in `ls $indir`
do
    if [ "$f" == ".." ]||[ "$f" == "." ]; then
        continue
    fi
    echo "---------- start processing $indir/$f---------"
    rm ./buffer/*
    cp $indir/$f ./buffer/.

    java -jar ./CKIPClient/CKIPClient.jar ./CKIPClient/ckipsocket.propeties buffer/ $outdir
    echo "----------- $indir/$f processed --------------"
    sleep 10
done
