#
# Makefile
#
#
#

###########################

LOG = | tee -a log.log

define separator
	@echo '\n================================================================================' $(LOG)
endef

all:
	$(call separator)
	@echo 'making all' $(LOG)
	@make download
	@make bruks
	@make bkrs

bkrs: download
	$(call separator)
	@( date; echo 'starting making bkrs'; )  $(LOG)
	@( ./bkrs.py  && cd final/大БКРС/  && make; )  $(LOG)
	@( date; echo 'done with bkrs'; )  $(LOG)

bruks: download
	$(call separator)
	@( date; echo 'starting making bruks'; )  $(LOG)
	@( ./bruks.py  && cd final/БРуКС/  && make; )  $(LOG)
	@( date; echo 'done with bkrs'; )  $(LOG)

download:
	$(call separator)
	@( date; echo 'downloading sources'; )  $(LOG)
	@./get_last_dicts.sh  $(LOG)
	@( date; echo 'download completed'; )  $(LOG)

install:
	@( date; echo 'installing all dictionaries for current user'; )  $(LOG)
	#
	@( cd "final/БРуКС/" && \
	make install; )  $(LOG)
	#
	@( cd "final/大БКРС" && \
	make install; )  $(LOG)
	#
	@( date; echo 'done'; )  $(LOG)

