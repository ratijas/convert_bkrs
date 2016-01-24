# Makefile
#
# Copyleft (C) 2016 Ratijas <ratijas.t@me.com>

# EI == Extended Index

timestamp = @echo "`date`:"

LOG = | tee -a


define separator
	@echo "\n================================================================================"
endef

VERBOSITY = -v 3

DESTANATION = final

RESOURCES = res

EXTENDED_INDEX_EDITION =  с расширенным индексом

BKRS_DSL  = downloads/bkrs.dsl
BRUKS_DSL = downloads/bruks.dsl

BKRS = 大БКРС
BRUKS = БРуКС
BKRS_EI = 大БКРС+
BRUKS_EI = БРуКС+

BKRS_DEST     = "$(DESTANATION)/$(BKRS)"
BRUKS_DEST    = "$(DESTANATION)/$(BRUKS)"
BKRS_EI_DEST  = "$(DESTANATION)/$(BKRS_EI)"
BRUKS_EI_DEST = "$(DESTANATION)/$(BRUKS_EI)"

BKRS_PREFS_HTML     = "$(DESTANATION)/$(BKRS).prefs.html"
BRUKS_PREFS_HTML    = "$(DESTANATION)/$(BRUKS).prefs.html"
BKRS_EI_PREFS_HTML  = "$(DESTANATION)/$(BKRS_EI).prefs.html"
BRUKS_EI_PREFS_HTML = "$(DESTANATION)/$(BRUKS_EI).prefs.html"


define BKRS_WRITE_OPTIONS
cleanHTML=yes;
css=$(RESOURCES)/dict.css;
xsl=$(RESOURCES)/dict.xsl;
prefsHTML=$(BKRS_PREFS_HTML);
defaultPrefs={
	"color_mode": "1",
	"tc1": "0",
	"tc2": "1",
	"tc3": "2",
	"tc4": "3",
	"tc0": "5",
	"version": "1",
};
frontBackMatter=$(RESOURCES)/front_back_matter.html;
OtherResources=$(RESOURCES)/OtherResources;
jing=yes
endef
export BKRS_WRITE_OPTIONS


define BRUKS_WRITE_OPTIONS
cleanHTML=yes;
css=$(RESOURCES)/dict.css;
xsl=$(RESOURCES)/dict.xsl;
prefsHTML=$(BRUKS_PREFS_HTML);
defaultPrefs={
	"color_mode": "1",
	"tc1": "0",
	"tc2": "1",
	"tc3": "2",
	"tc4": "3",
	"tc0": "5",
	"version": "1",
};
frontBackMatter=$(RESOURCES)/front_back_matter.html;
OtherResources=$(RESOURCES)/OtherResources;
jing=yes
endef
export BRUKS_WRITE_OPTIONS


define BRUKS_EI_WRITE_OPTIONS
$(BRUKS_WRITE_OPTIONS);
prefsHTML=$(BRUKS_EI_PREFS_HTML);
indexes=ru
endef
export BRUKS_EI_WRITE_OPTIONS


define BKRS_EI_WRITE_OPTIONS
$(BKRS_WRITE_OPTIONS);
prefsHTML=$(BKRS_EI_PREFS_HTML);
indexes=zh
endef
export BKRS_EI_WRITE_OPTIONS


bkrs: download
	@mkdir -p log
	make .bkrs $(LOG) log/bkrs.log


.bkrs:
	$(call separator)
	mkdir -p "$(DESTANATION)"
	sed "s/{{BundleDisplayName}}/大БКРС/; s/{{BundleShortVersionString}}/$$(cat downloads/version.txt)/" < $(RESOURCES)/prefs.html > $(BKRS_PREFS_HTML)
	$(timestamp) "start making 大БКРС"
	@echo "BKRS_WRITE_OPTIONS='$${BKRS_WRITE_OPTIONS}'"
	pyglossary --ui=cmd $(VERBOSITY) $(BKRS_DSL) $(BKRS_DEST) --write-format=AppleDict --write-options="$${BKRS_WRITE_OPTIONS}"
	cd $(BKRS_DEST) && make
	$(timestamp) "done with 大БКРС"


bkrs-ei: download
	@mkdir -p log
	make .bkrs-ei $(LOG) log/bkrs-ei.log


.bkrs-ei:
	$(call separator)
	mkdir -p "$(DESTANATION)"
	sed "s/{{BundleDisplayName}}/大БКРС+/; s/{{BundleShortVersionString}}/$$(cat downloads/version.txt) $(EXTENDED_INDEX_EDITION)/" < $(RESOURCES)/prefs.html > $(BKRS_EI_PREFS_HTML)
	$(timestamp) "start making 大БКРС+"
	@echo "BKRS_EI_WRITE_OPTIONS='$${BKRS_EI_WRITE_OPTIONS}'"
	pyglossary --ui=cmd $(VERBOSITY) $(BKRS_DSL) $(BKRS_EI_DEST) --write-format=AppleDict --write-options="$${BKRS_EI_WRITE_OPTIONS}"
	cd $(BKRS_EI_DEST) && make
	$(timestamp) "done with 大БКРС+"


bruks: download
	@mkdir -p log
	make .bruks $(LOG) log/bruks.log


.bruks:
	$(call separator)
	mkdir -p "$(DESTANATION)"
	sed "s/{{BundleDisplayName}}/БРуКС/; s/{{BundleShortVersionString}}/$$(cat downloads/version.txt)/" < $(RESOURCES)/prefs.html > $(BRUKS_PREFS_HTML)
	$(timestamp) "start making БРуКС"
	@echo "BRUKS_WRITE_OPTIONS='$${BRUKS_WRITE_OPTIONS}'"
	pyglossary --ui=cmd $(VERBOSITY) $(BRUKS_DSL) $(BRUKS_DEST) --write-format=AppleDict --write-options="$${BRUKS_WRITE_OPTIONS}"
	cd $(BRUKS_DEST) && make
	$(timestamp) "done with БРуКС"


bruks-ei: download
	@mkdir -p log
	make .bruks-ei $(LOG) log/bruks-ei.log


.bruks-ei:
	$(call separator)
	mkdir -p "$(DESTANATION)"
	sed "s/{{BundleDisplayName}}/БРуКС+/; s/{{BundleShortVersionString}}/$$(cat downloads/version.txt) $(EXTENDED_INDEX_EDITION)/" < $(RESOURCES)/prefs.html > $(BRUKS_EI_PREFS_HTML)
	$(timestamp) "start making БРуКС+"
	@echo "BRUKS_EI_WRITE_OPTIONS='$${BRUKS_EI_WRITE_OPTIONS}'"
	pyglossary --ui=cmd $(VERBOSITY) $(BRUKS_DSL) $(BRUKS_EI_DEST) --write-format=AppleDict --write-options="$${BRUKS_EI_WRITE_OPTIONS}"
	cd $(BRUKS_EI_DEST) && make
	$(timestamp) "done with БРуКС+"


download:
	$(call separator)
	$(timestamp) "downloading sources"
	./get_last_dicts.sh
	$(timestamp) "download completed"


install:
	$(timestamp) "installing all dictionaries for current user"
	#
	@for dir in $(BRUKS_DEST) $(BRUKS_EI_DEST) $(BKRS_DEST) $(BKRS_EI_DEST) ; do \
		[ -d "$$dir" ] && \
		pushd "$$dir" && \
		make install && \
		popd || \
		echo "no directory $$dir" ; \
	done
	#
	$(timestamp) "done"


7Z_DEST = $(DESTANATION)/7z


7z:
	$(timestamp) "archiving dictionaries with 7z"
	mkdir -p "$(7Z_DEST)"
	@# symlink everything together
	@for dir in $(BRUKS_DEST) $(BRUKS_EI_DEST) $(BKRS_DEST) $(BKRS_EI_DEST) ; do \
		if [ -d "$$dir/objects" ] ; then \
			ln -fs "`pwd`/$$dir/objects"/*.dictionary "$(7Z_DEST)" ;\
		else \
			echo "no directory $$dir/objects" ;\
		fi ;\
	done
	@# one dictionary per archive
	@cd "$(7Z_DEST)" &&\
		for dict in *.dictionary ; do \
			7z a -l -t7z -mx=9 "$${dict}".7z "$${dict}" ;\
		done
	@# remove symlinks
	@rm "$(7Z_DEST)"/*.dictionary
	$(timestamp) "done"


TORRENT_BASE = $(DESTANATION)/torrent
TORRENT = "$(TORRENT_BASE)/$(BKRS) и $(BRUKS) для Mac OS X"/
TORRENT_EI = "$(TORRENT_BASE)/$(BKRS_EI) и $(BRUKS_EI) для Mac OS X"/


.PHONY: torrent
torrent:
	mkdir -p $(TORRENT)
	cp "$(7Z_DEST)/$(BKRS).dictionary.7z" $(TORRENT)
	cp "$(7Z_DEST)/$(BRUKS).dictionary.7z" $(TORRENT)
	cp "torrent/readme.html" $(TORRENT)

	mkdir -p $(TORRENT_EI)
	cp "$(7Z_DEST)/$(BKRS_EI).dictionary.7z" $(TORRENT_EI)
	cp "$(7Z_DEST)/$(BRUKS_EI).dictionary.7z" $(TORRENT_EI)
	cp "torrent/readme.html" $(TORRENT_EI)

	@echo "now create torrent files with your torrent client from these directories:"
	@echo $(TORRENT)
	@echo $(TORRENT_EI)


all:
	$(call separator)
	@echo "making all"
	make download
	make bruks
	make bruks-ei
	make bkrs
	make bkrs-ei
