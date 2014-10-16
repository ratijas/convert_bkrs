#
# Makefile
#
#
#

###########################
LOG = "log.log"

download:
	./get_last_dicts.sh | tee $(LOG); \
        log 'download completed';

bkrs: download
	log(){ date >>$(LOG); echo -e $* >> $(LOG);}; \
        error(){ date >> $(LOG); echo -e $* >> $(LOG); exit 1;}; \
	\
        log 'converting bkrs'; \
        ./bkrs.py && \
        cd "final/大БКРС" && \
        make | tee $(LOG) || \
        error 'converting bkrs failed'; \
        \
        log 'done';

bruks: download
	log(){ date >>$(LOG); echo -e $* >> $(LOG);}; \
        error(){ date >> $(LOG); echo -e $* >> $(LOG); exit 1;}; \
	\
        log 'converting bruks';\
        \
        ./bruks.py && \
        cd "final/БРуКС/" && \
        make | tee $(LOG) || \
        error 'converting bruks failed'; \
        \
	log 'done';

all: download bruks bkrs
	log(){ date >>$(LOG); echo -e $* >> $(LOG);}; \
	error(){ date >> $(LOG); echo -e $* >> $(LOG); exit 1;}; \
	\
	log 'starting making target `all`';

install:
	echo -e "`date`\n""installing all dictionaries for current user" >> $(LOG)
	#
	cd "final/БРуКС/" && \
	make install | tee $(LOG)
	#
	cd "final/大БКРС" && \
	make install | tee $(LOG)
	#
	echo -e "`date`\n""done" >> $(LOG)

install-all:
	echo -e "`date`\n""installing all dictionaries all users" >> $(LOG)
	#
	cd "final/БРуКС/" && \
	cp -pPR "БРуКС.dictionary" /Library/Dictionaries/
	#
	cd "final/大БКРС/" && \
	cp -pPR "大БКРС.dictionary" /Library/Dictionaries/
	#
	echo -e "`date`\n""done" >> $(LOG)

