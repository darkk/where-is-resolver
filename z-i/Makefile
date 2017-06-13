grep-cheap: https-without-soa
	grep -iE '\.(info|bike|singles|GRAPHICS|LIGHTING|land|today|technology|photos|cab|center|email|cheap|club|international|store|us|co|co.uk|me|pw|me.uk)$$' $^

random-zapret-info.zone: dump.csv
	grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' $^ | shuf -n 4096 | sort -u | shuf -n 2048 | sed 's,^,@   IN A    ,' >$@



bare-without-soa: bare-domains bare-with-soa
	cat $^ | awk '{print $$1}' | sort | uniq -c | awk '($$1 == 1) {print $$2}' >$@

bare-with-soa: bare-domains
	python has_soa.py <$^ >$@~
	mv $@~ $@

bare-domains: dump.csv
	cat $^ | iconv -f cp1251 | awk -F ';' '($$3 == "" && $$2 != "") {print $$2}' | sort -u >$@



http-without-soa: http-domains http-with-soa
	cat $^ | awk '{print $$1}' | sort | uniq -c | awk '($$1 == 1) {print $$2}' >$@

http-with-soa: http-domains
	python has_soa.py <$^ >$@~
	mv $@~ $@

http-domains: dump.csv
	cat $^ | iconv -f cp1251 | grep http: | cut -d ';' -f 2 | grep -vE '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort -u >$@



https-without-soa: https-domains https-with-soa
	cat $^ | awk '{print $$1}' | sort | uniq -c | awk '($$1 == 1) {print $$2}' >$@

https-with-soa: https-domains
	python has_soa.py <$^ >$@~
	mv $@~ $@

https-domains: dump.csv
	cat $^ | iconv -f cp1251 | grep https: | cut -d ';' -f 2 | grep -vE '^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort -u >$@



dump.csv:
	cp -a ../../z-i/$@ $@

clean:
	rm -f random-zapret-info.zone bare-without-soa bare-with-soa bare-domains http-without-soa http-with-soa http-domains https-without-soa https-with-soa https-domains
