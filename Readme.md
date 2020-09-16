Программа для бэкапа

Доступные команды:
    -create task task_name - создание таска бэкапа
    -delete task task_name - удаление таска
    -setup task task_name - настройки таска
    -tasks list - список созданных тасков
    -launch backup task_name - запустить бэкап

Настройки таска:
    -add/remove file file_name - Добавить/удалить файл таска
    -add/remove destination dst_name - добавить/удалить пункт назначения

Доступные элементы бэкапа:
    -Файлы

Доступные места назначения:
    -yandexdisk
    -googledrive

Примеры:
    create task x
    setup task x
    add file C:/Users/MainUser/Desktop/Cat.jpg
    add destination yandexdisk(или googledrive)
    ...настройки пункта назначения
    back
    launch backup x