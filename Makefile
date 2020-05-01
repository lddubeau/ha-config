LIVE_HOST=ha@ha
LIVE_HOME=~/src/ha-docker/
LIVE_CONFIG=$(LIVE_HOME)ha-config/

RSYNC_EXTRA_OPTS=
RSYNC_CMD=rsync -va --filter=". ./rsync-filter" --delete $(RSYNC_EXTRA_OPTS) ./out/ $(LIVE_HOST):$(LIVE_CONFIG)

default:
	./make.sh

check-sync: RSYNC_EXTRA_OPTS=--dry-run
check-sync:
	$(RSYNC_CMD)

sync:
	$(RSYNC_CMD)

backup:
	ssh $(LIVE_HOST) 'cp -rp $(LIVE_CONFIG) $(LIVE_HOME)ha-config.$$(date --iso-8601=seconds)'

diff:
	diff -uraN --ignore-matching-lines="^# Generated at" prev out
