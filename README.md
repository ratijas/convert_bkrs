convert-bkrs
=================

конвертация большого китайско-русско-китайского словаря в формат .dictionary

![大БКРС](both/OtherResources/Images/icon.png)

## конвертация

`$ make`

## установка для текущего пользователя

`$ make install`

## установка для всех пользователей системы

`$ make install-all`

## файлы и папки

* ./downloads
	- сюда скачиваются базы в dsl формате
* ./final
	- здесь будут лежать готовые пакеты
* ./img
	- скриншоты приложения Dictionary.app для ознакомления

## зависимости

* python
	- pymorphy2
* java
* curl
* gunzip
