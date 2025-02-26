# Сервис для магазина мерча Авито

## Запуск приложения
1. Клонировать репозиторий
```
git clone https://github.com/Polly-coder/AvitoShop.git
```
2. Перейти в папку проекта
```
cd AvitoShop
```
3. База данных и приложение запускаются через docker-compose
```
docker-compose up --build
```
Приложение будет запущено по адресу http://127.0.0.1:8080
Документация http://127.0.0.1:8080/docs

## REST API

**GET api/info**  
Получение информации о пользователе, включая приобретенные товары и историю обменов  

Для определения текущего пользователя, необходимо передать токен в заголовках запроса  

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
Авторизация или создание пользователя и получение JWT-токена  

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

**POST api/sendCoin**  
Перевод монет другому пользователю  
Требуется отправка jwt-токена в заголовках запроса

Request body:
```json
{
  "to_user_id": "int",
  "amount": "int"
}
```
Response body:
```json
{
  "transfer_result": "string"
}
```