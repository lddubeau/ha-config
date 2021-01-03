LIVE_HOST=ha@ha.lddubeau.com
LIVE_ROOT_HOST=ldd@ha.lddubeau.com
LIVE_HOME=/home/ha/src/ha-docker/
LIVE_CONFIG=$(LIVE_HOME)ha-config/

BACKUP_HOST=ldd@shunya
BACKUP_PATH=/home/ldd/ha-backup/

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
#	ssh $(LIVE_ROOT_HOST) 'sudo cp -rp $(LIVE_CONFIG) $(LIVE_HOME)ha-config.$$(date --iso-8601=seconds)'
# Compress on the receiving host.
	ssh $(LIVE_ROOT_HOST) 'sudo tar -C $(LIVE_CONFIG) -cpf - .' | ssh $(BACKUP_HOST) 'xz > $(BACKUP_PATH)$(BACKUP_HOME)ha-config.$$(date --iso-8601=seconds).txz'

diff:
	diff -uraN --ignore-matching-lines="^# Generated at" prev out
