#大БКРС и БРуКС

##системные требования

- OS X 10.4 Tiger (в ней появился Dictionary.app) или новее
- 720 МБ на диске для упрощенной версии, **либо**
- 1,33 ГБ на диске для версии с расширенным индексом (*см. ниже*)

##описание (взято с [сайта словаря](http://bkrs.info))

**大БКРС** — открытый редактируемый большой китайско-русско-китайский словарь

основные принципы словаря:

- полнота - словарь включает в себя не только слова, но и устойчивые сочетания
- современность - словарь не включает в себя древнекитайский язык

словарь сконвертиврован питоном из dsl файла, который можно скачать на сайте словаря
программу для конвертирования словарей dsl -> apple можно найти на [github'е](https://github.com/ratijas/convert_bkrs)

##доп. информация

###инструкция по установке

- скачать
- распаковать архивы со словарями (7z, две штуки), бесплатные программы для распаковки перечислены ниже
- открыть новое окно Finder
- выбрать меню "переход" -> "переход к папке…", или нажать `⇧⌘G`
- ввести `~/Library/Dictionaries` и нажать enter
- перетащить в эту папку распакованные (*см. пункт 2*) пакеты с расширением **.dictionary**
- перезапустить приложение `Словарь`
- зайти в настройки (`⌘,` ), и в списке отметить галочку напротив 大БРКС, БРуКС
- ...
- PROFIT!!!

####из замеченных проблем с установкой

- окно предпросмотра не сразу начинает отображать слова из новоустановленных словарей. возможно, потребуется выход + вход в систему

#### программы для работы с 7z-архивами

- [7zX](http://www.macupdate.com/app/mac/20526/7zx) — просто 7z
- [Keka](http://www.kekaosx.com/ru/) — достойная замена стандартному архиватору Mac OS X
- `$ brew install `[`p7zip`](http://p7zip.sourceforge.net/) — для командной строки

###инструкция по использованию

* просто откройте приложение и наберите слово
* нажмите `⌃пробел` (ctrl+пробел, для вызова spotlight) и наберите слово. статья из словаря появится в списке результатов. достаточно навести на неё курсор, чтобы увидеть перевод
* читая текст, наведите курсор на слово, или выделите кусок текста; далее нажмите `⌃⌘D` ( ctrl+cmd+D ), или (для тех, кто с трекпадом) коснитесь сенсорной поверхоности тремя пальцами
* что бы убрать из списка результатов всё лишнее, *добавьте в конце поиска точку*`.` особенно полезно при поиске по пининю.
* цветной пиньинь. прям как на сайте, но ещё круче. с возможностью настроить по своему вкусу. достаточно зайти в настройки (`⌘,`)

####а также в версии с расширенным индексом:

- БРуКС

    есть поддержка морфологии. слово можно найти по любым его формам. однако, из соображений экономии места, это касается только отдельных слов, но не словосочетаний.

- 大БКРС

    поиск по китайско-русскому направлению на стероидах (на примере 软件开发者):

    * 《软件》=> слова, которые начинаются на 《软件》
    * 《软件。》 => только 《软件》
    * если знаешь пиньинь, но не помнишь, как пишется, можно искать по пиньиню. пиньинь **нужно** разделять пробелами. вместо тонов можно использовать цифры. например:
        - ruan jian (*без тонов*)
        - ruǎn jiàn (*с диакритическими знаками*)
        - ruan3 jian4 (*с цифрами вместо диакритических знаков*)
        - ruan jian. (*точное совпадение, про точку читай выше*)

некоторые пользователи жаловались, что индекс получается очень уж раздутым и занимает слишком много места, а самый инициативный мой коллега даже сконвертил и выложил свою [раздачу](http://rutracker.org/forum/viewtopic.php?t=4995096); поэтому было решено сделать две версии: с индексом и без.  одна занимает меньше места, другая удобнее в использовании.  готовы ли пожертвовать пол-гигабайта ради удобства — решать вам, благо выбор есть.

##ссылки

- [собственно, он самый, в оригинале](http://bkrs.info/)
- [скачать торрент](http://rutracker.org/forum/viewtopic.php?t=4743501)
- [github bug tracker (жалобы и предложения)](https://github.com/ratijas/convert_bkrs/issues)
- [ветка поддержки на форуме](http://bkrs.info/taolun/thread-153.html)