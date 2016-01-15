#!/bin/bash

#globals
DEST_FOLDER=downloads
URL_FILE=urls.txt
FILE_GZ1=
FILE_GZ2=
FILE1=
FILE2=
BKRS_DSL="bkrs.dsl"
BRUKS_DSL="bruks.dsl"
VERSION_TXT="version.txt"
ECHO="builtin echo "

clean()
{
  if [ "${PWD##*/}" == "$DEST_FOLDER" ]; then
    rm "$URL_FILE" "$FILE_GZ1" "$FILE_GZ2" >/dev/null 2>&1
    cd ..
  fi
  #rm -rf "$DEST_FOLDER" >/dev/null 2>&1
}

error()
{
  ${ECHO} $*
  clean
  exit 1
}

check_if_exists()
{
	if [ `( find bkrs -name $BKRS_DSL -ctime 0;
		find bruks -name $BRUKS_DSL -ctime 0; ) |
		wc -l` == 2 ]
	then
		echo "словарные базы загружены менее суток назад.
чтобы всё-равно скачать новые базы, удалите существующие командой
$ rm bkrs/$BKRS_DSL bruks/$BRUKS_DSL"
		exit 0
	fi
}

init()
{
  for FOLDER in "$DEST_FOLDER" "bkrs" "bruks"
  do
    ${ECHO} "создаю папку \"$FOLDER\""
    mkdir -p $FOLDER
  done ||

  error "не удаётся создать папку $FOLDER"

  cd $DEST_FOLDER
}

search()
{
  ${ECHO} "ищу последние базы"

curl http://bkrs.info/p47 | #скачать страницу загрузок
grep '\.gz' |        #найти ежедневные базы в формате .gz
sed -E "s/^.*href='(.*)'.*$/\\1\\
/g" |                #вытянуть прямую ссылку из html-тега
sort -u |            #убрать лишние пустые строки и повторы
grep '\.gz' |        #убрать оставшуюся пустую строку
grep -v 'examples' | #убрать примеры
tee "$VERSION_TXT" | #потом вытянуть версию
sed 'i\
http://bkrs.info/' | #относительный url -> абсолютный url
cat > "$URL_FILE" || #временно сохранить ссылки

error "не удаётся найти ссылки на словарные базы"


  URL1=`sed '1p;d' "$URL_FILE"` &&
  URL2=`sed '2p;d' "$URL_FILE"` ||

  error "не удаётся вытащить ссылки из файла"


  FILE_GZ1="${URL1##*/}"
  FILE_GZ2="${URL2##*/}"

  head -n 1 $VERSION_TXT |
  sed -E 's/^.*([[:digit:]]{6}).*$/v\1/' > "$VERSION_TXT.1"

  mv "$VERSION_TXT.1" "$VERSION_TXT"
}

download()
{
  msg="скачиваю базы за сегодня:"
  cmd="curl --retry 8 -C - "

  for url in "$@";
  do
    msg="${msg}\n${url}"
    file="${url##*/}"
    cmd=$cmd" -o \"$file\" \"$url\" "
  done

  ${ECHO} $msg

  eval $cmd || #скачать

  error "что-то пошло не так, и словарные базы не загрузились. проверьте сообщения выше"
}

unarcive()
{
  ${ECHO} "разархивация..."

  gunzip -f *.gz ||
  error "не удаётся разархивировать базы"

  FILE1=${FILE_GZ1%*.gz}
  FILE2=${FILE_GZ2%*.gz}

  ${ECHO} "готово"
}

rmbom()
{
  ${ECHO} "убираю BOM..."

  FILES="$@"
  for file in $FILES;
  do
    if [ "`head -c3 \"$file\"`" == $'\xef\xbb\xbf' ];
    then
      tail -c +4 "$file" > "${file}_" &&
      mv "${file}_" "$file"           ||

      error "ошибка"
    fi ||
    error "ошибка"
  done

  ${ECHO} "готово"
}

rename()
{
  ${ECHO} "переименовываю файлы"

  bkrs_f=` ls | grep -e "bkrs"      | grep -v -e "\.gz" | head -n 1` &&
  bruks_f=`ls | grep -e "br[u]\?ks" | grep -v -e "\.gz" | head -n 1` ||

  error 'файлы как будто были скачаны, но теперь их невозможно найти?'
 
  mv "$bkrs_f"  "$BKRS_DSL"  &&
  mv "$bruks_f" "$BRUKS_DSL" ||

  error "не удалось переименовать $bkrs_f и $bruks_f в $BRKS_DSL и $BRUKS_DSL соответственно"
}

move()
{
  ${ECHO} "перемещаю в папки /bkrs/ и /bruks/ ..."

  mv -f "$BKRS_DSL"  ../bkrs/"$BKRS_DSL"   &&
  mv -f "$BRUKS_DSL" ../bruks/"$BRUKS_DSL" ||

  error "не удаётся переместить .dsl файлы"

  ${ECHO} "готово"
}

clean_maybe()
{
  ${ECHO} "================================================================================"
  read -p "очистить исходные и временные файлы? [yes/no] (yes после 30 секунд) " -t 30 ||
    REPLY="yes"
  ${ECHO}

  if [ "`${ECHO} "${REPLY: 0:1}" | tr Y y`" == "y" ]
  then
    clean
    ${ECHO} "готово"
  fi
}

check_if_exists
init
search
download "$URL1" "$URL2"
unarcive
rmbom "$FILE1" "$FILE2"
rename
move

${ECHO} "
файлы $BRKS_DSL и $BRUKS_DSL успешно скачаны, разархивированы,
сконвертированы в utf-8 и сохранены в папках bkrs и bruks"

clean_maybe

