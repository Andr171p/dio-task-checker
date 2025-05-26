# Оценка заданий сотрудникам

## API

> POST /api/v1/tasks

### Тело запроса:
```json
{
  "subdivision": "string",
  "theme": "string",
  "description": "string",
  "hours": 0,
  "jobs": [
    {
      "hours": 0,
      "content": "string"
    }
  ]
}
```

 * <b>subdivision</b> - подразделение
 * <b>theme</b> - тема
 * <b>description</b> - описание
 * <b>hours</b> - общее количество часов
 * <b>jobs</b> - работы:
   * <b>hours</b> - количество часов на одну работу
   * <b>content</b> - содержание

### Тело ответа
```json
{
  "rate": 1,
  "comments": "string"
}
```

 * <b>rate</b> - оценка от 1 до 10
 * <b>comments</b> - комментарии и рекомендации


## Запуск

```shell
git clone https://github.com/Andr171p/dio-task-checker.git
cd dio-task-checker
```

```shell
nano .env
```

### Шаблон .env файла
```.env
# GigaChat creadentials:
GIGACHAT_API_KEY = "API Token"
GIGACHAT_SCOPE = ""
```

```shell
docker-compose up -d
```

### Проверка работы

```shell
curl http://localhost:8000
```