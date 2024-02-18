## Первое тестовое задание - проект Phonebook

Автор проекта: Ильдар Аюпов

Мои комментарии к техническому заданию:
- рекомендую версионировать API, изменив структуру адресов эндпоинтов: ```api/v1/...```
- предлагаю в названия ручек не включать указания на операции (write, check). Лучше, если название ручки - это просто ресурс. Операции же, которые будут выполняться над данным ресурсом, будут следовать из http-метода (GET, POST и т.д.)
- заключение номера телефона в одинарные кавычки в примере GET-запроса в техническом задании - это, по всей видимости, опечатка. Обычно так не делается. Если задавать значение в одинарных кавычках, то кавычки будут частью этого значения. Тогда либо придется их специально убирать при обработке реквеста, либо они так и будут храниться в базе с одинарными кавычками и телефонный номер при получении будет выглядеть так: {"phone": "'111'"}. В моей реализации АПИ параметры GET запроса в кавычки не включаются.
- проект контейнеризирован и оркестрирован (docker, docker compose).
- поскольку Redis здесь выступает полноценным хранилищем, а не просто временным кэшем, то в docker compose к нему прикручен volume для долговременного хранения.
- АПИ работает через Nginx через 80 порт (или просто без указания порта). Все остальные порты для безопасности закрыты.

Как запустить проект:
- Клонировать репозиторий:
```git clone git@github.com:ildar-aiupov/phonebook.git```
- В корне проекта переименовать файл `.env.example` в файл `.env` (команда `mv .env.example .env`). Все настройки рабочие, ничего менять не нужно.
- Находясь в корневой папке проекта, запустить его сборку:
```sudo docker compose up -d```
- Краткое описание эндпоинтов проекта:
```
[GET]: http://localhost/check_data?phone=12345678901
```
```
[POST]: http://localhost/write_data
[body]:
{
    "phone": "12345678901",
    "address": "some address"
}
```
```
[PATCH]: http://localhost/write_data
[body]:
{
    "phone": "12345678901",
    "address": "some new address"
}
```
- Подробное описание API доступно по ссылке:
```http://localhost/docs```


## Второе тестовое задание

По второму заданию предлагаю 3 возможных решения. Все они занимают буквально несколько секунд (тестировалось на Postgres 16.1)

Решение №1 (выполняется около 3 сек.)  
UPDATE full_names  
SET status = short_names.status  
FROM short_names  
WHERE short_names.name = SPLIT_PART(full_names.name, '.', 1);

Решение №2 (выполняется около 2 сек.)  
CREATE TABLE tmptable AS  
SELECT full_names.id, full_names.name, short_names.status  
FROM full_names  
LEFT JOIN short_names ON short_names.name = SPLIT_PART(full_names.name, '.', 1);  
DROP TABLE full_names;  
ALTER TABLE tmptable RENAME TO full_names;

Решение №3 (выполняется около 2 сек.)  
CREATE TABLE tmptable AS  
SELECT full_names.id, full_names.name, short_names.status  
FROM full_names  
LEFT JOIN short_names ON short_names.name = SPLIT_PART(full_names.name, '.', 1);  
TRUNCATE full_names;  
INSERT INTO full_names SELECT * from tmptable;
