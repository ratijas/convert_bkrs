
#
# Makefile
#
#
#

###########################

# You need to edit these values.

DICT_NAME		=	"大БРуКС"
DICT_SRC_PATH	=	bruks.xml
CSS_PATH		=	bruks.css
PLIST_PATH		=	bruksInfo.plist

DICT_BUILD_OPTS		=
# Suppress adding supplementary key.
# DICT_BUILD_OPTS		=	-s 0	# Suppress adding supplementary key.

###########################

# The DICT_BUILD_TOOL_DIR value is used also in "build_dict.sh" script.
# You need to set it when you invoke the script directly.

# DICT_BUILD_TOOL_DIR	=	"/DevTools/Utilities/Dictionary Development Kit"
# ratijas: папка bin из dictionary development kit включена в проект. чтобы далеко не бегать
DICT_BUILD_TOOL_BIN	=	"bin"

###########################

DICT_DEV_KIT_OBJ_DIR	=	./objects_bruks
export	DICT_DEV_KIT_OBJ_DIR

DESTINATION_FOLDER	=	~/Library/Dictionaries
RM			=	/bin/rm

###########################

all:
	"$(DICT_BUILD_TOOL_BIN)/build_dict.sh" $(DICT_BUILD_OPTS) $(DICT_NAME) $(DICT_SRC_PATH) $(CSS_PATH) $(PLIST_PATH)
	echo "Done."


install:
	echo "Installing into $(DESTINATION_FOLDER)".
	mkdir -p $(DESTINATION_FOLDER)
	ditto --noextattr --norsrc $(DICT_DEV_KIT_OBJ_DIR)/$(DICT_NAME).dictionary  $(DESTINATION_FOLDER)/$(DICT_NAME).dictionary
	touch $(DESTINATION_FOLDER)
	echo "Done."
	echo "To test the new dictionary, try Dictionary.app."

clean:
	$(RM) -rf $(DICT_DEV_KIT_OBJ_DIR)
