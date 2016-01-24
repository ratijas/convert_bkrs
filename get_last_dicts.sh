#!/bin/sh

#globals
DEST_DIR=downloads
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
    return
    if [ "${PWD##*/}" == "$DEST_DIR" ]; then
        rm "${URL_FILE}" "$FILE_GZ1" "$FILE_GZ2" >/dev/null 2>&1
        cd ..
    fi
}

error()
{
    ${ECHO} "$*"
    clean
    exit 1
}

check_if_exists()
{
    if [ $( ( find "${DEST_DIR}" -name "${BKRS_DSL}" -ctime 0;
              find "${DEST_DIR}" -name "${BRUKS_DSL}" -ctime 0; ) |
            wc -l ) == 2 ]
    then
        echo "словарные базы загружены менее суток назад.
чтобы всё-равно скачать новые базы, удалите существующие командой
$ rm '$DEST_DIR/$BKRS_DSL' '$DEST_DIR/$BRUKS_DSL'"
        exit 0
    fi
    if [ $( ls *.gz |
            wc -l ) == 2 ]
    then
        return 2
    fi
}

init()
{
    for DIR in "$DEST_DIR"
    do
        ${ECHO} "создаю папку \"$DIR\""
        mkdir -p ${DIR}
    done ||

    error "не удалось создать папку $DIR"

    cd ${DEST_DIR}
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
    tee "${VERSION_TXT}" | #потом вытянуть версию
    sed 'i\
http://bkrs.info/' | #относительный url -> абсолютный url
    cat > "${URL_FILE}" || #временно сохранить ссылки

    error "не удаётся найти ссылки на словарные базы"


    URL1=$(sed '1p;d' "${URL_FILE}") &&
    URL2=$(sed '2p;d' "${URL_FILE}") ||

    error "не удаётся вытащить ссылки из файла"


    FILE_GZ1="${URL1##*/}"
    FILE_GZ2="${URL2##*/}"

    head -n 1 "${VERSION_TXT}" |
    sed -E 's/^.*([[:digit:]]{6}).*$/v\1/' > "${VERSION_TXT}_"

    mv "${VERSION_TXT}_" "${VERSION_TXT}"
}

download()
{
    msg="скачиваю базы за сегодня:"
    template="wget --tries=8 --continue -- "

    ${ECHO} "${msg}"

    for url in "$@";
    do
        file="${url##*/}"
        cmd="${template} \"${url}\""
        ${ECHO} "${cmd}"
        eval ${cmd}
    done ||

    error "что-то пошло не так, и словарные базы не загрузились. проверьте сообщения выше"
}

unarchive()
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

    for file in "$@";
    do
        if [ "$(head -c3 "${file}")" == $'\xef\xbb\xbf' ];
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

    bkrs_f=$( ls | grep -e "bkrs"      | grep -v -e "\.gz" | head -n 1) &&
    bruks_f=$(ls | grep -e "br[u]\?ks" | grep -v -e "\.gz" | head -n 1) ||

    error 'файлы как будто были скачаны, но теперь их невозможно найти?'

    mv "$bkrs_f"  "$BKRS_DSL"  &&
    mv "$bruks_f" "$BRUKS_DSL" ||

    error "не удалось переименовать $bkrs_f и $bruks_f в $BKRS_DSL и $BRUKS_DSL соответственно"
}

clean_maybe()
{
    ${ECHO} "================================================================================"
    read -p "очистить исходные и временные файлы? [yes/no] (yes после 30 секунд) " -t 30 ||
    REPLY="yes"
    ${ECHO}

    if [ "$(${ECHO} "${REPLY: 0:1}" | tr Y y)" == "y" ]
    then
        clean
        ${ECHO} "готово"
    fi
}

check_if_exists
if [ $? != 2 ] ; then
init
search
download "$URL1" "$URL2"
fi
unarchive
rmbom "$FILE1" "$FILE2"
rename

${ECHO} "
файлы $BKRS_DSL и $BRUKS_DSL успешно скачаны, разархивированы,
сконвертированы в utf-8 и сохранены в $DEST_DIR"

clean_maybe
