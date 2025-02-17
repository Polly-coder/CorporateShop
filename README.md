# Сервис для магазина мерча Авито

## Запуск приложения
1.
2.
3.


## REST API

**GET api/info**
Получение информации о пользователе, включая приобретенные товары и историю обменов
Определяет текущего пользователя по токену в headers
Response body:
```json
{
  "coins": 0,
  "inventory": [
    {
      "type": "string",
      "quantity": 0
    }
  ],
  "coinHistory": {
    "received": [
      {
        "fromUser": "string",
        "amount": 0
      }
    ],
    "sent": [
      {
        "toUser": "string",
        "amount": 0
      }
    ]
  }
}
```
**POST api/auth**
Аутентификация и получение JWT-токена
Request body:
```json
{
  "username": "string",
  "password": "string"
}
```
Response body:
```json
{
  "token": "string"
}
```