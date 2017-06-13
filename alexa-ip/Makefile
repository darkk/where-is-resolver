include make.opt # define NET and NSIP

all: ipv4.txt ipv6.txt

ipv6.txt: run-resolve
	sqlite3 top-1m.sqlite 'select ipv6 from ipv6' | jq . | grep '"' | sed 's,[^0-9a-fA-F:]\+,,g' | sort -u >$@

ipv4.txt: run-resolve
	sqlite3 top-1m.sqlite 'select ipv4 from ipv4' | jq . | grep '"' | sed 's,[^0-9.]\+,,g' | sort -u >$@

# Running everything in Docker like a true hipster!

run-pdns: pdns-recursor/.built
	docker run --rm -ti --network=$(NET) --ip=$(NSIP) --memory 256M local/pdns-recursor --max-cache-entries=100000 --max-packetcache-entries=5000

run-resolve: top-1m.sqlite
	docker run --rm -ti --network=$(NET) --dns=$(NSIP) -v $$PWD:/mnt --workdir /mnt --memory 128M python:2.7-alpine python2 resolve.py $^
	touch run-resolve

pdns-recursor/.built: pdns-recursor/Dockerfile
	cd pdns-recursor && docker build -t local/pdns-recursor:latest . && cd .. && touch -r $^ $@

top-1m.sqlite: top-1m.csv
	sqlite3 $@~ 'create table domain (rank integer primary key, domain text)'
	sqlite3 $@~ 'create table ipv4 (rank integer primary key, ipv4 text)'
	sqlite3 $@~ 'create table ipv6 (rank integer primary key, ipv6 text)'
	sqlite3 -separator ',' $@~ '.import top-1m.csv domain'
	mv $@~ $@

top1-m.csv: top-1m.csv.zip
	unzip $^ $@

top-1m.csv.zip:
	wget -O $@ https://s3.amazonaws.com/alexa-static/top-1m.csv.zip
