ТЗ LightTech


1. Для скачивания проекта необходимо запустить следующее:
```shell
git clone 
```

2. Для запуска проекта необходимости запустить сборку (ВАЖНО, проверить наличие docker c compose):
```shell
sudo docker compose up --build 
```

3. После запуска. Для использования баланса и т.п., необходимо зарегистрироваться:
```shell
curl --request POST \
  --url http://127.0.0.1:8000/user/register/ \
  --header 'Content-Type: application/json' \
  --data '{
	"username": "ВАШ юзернейм",
	"password": "пароль",
	"password_check": "пароль"
}'
```
4. Получаем токен, и с токеном мы можем использовать апи ручки.
-  Депозит баланса
```shell
curl --request GET \
  --url http://127.0.0.1:8000/user/balance/ \
  --header 'Authorization: Token ТОКЕН' \
  --header 'Content-Type: application/json'
```

-  Перевод баланса
```shell
curl --request POST \
  --url http://127.0.0.1:8000/user/transfer/ \
  --header 'Authorization: Token ТОКЕН' \
  --header 'Content-Type: application/json' \
  --data '{
	"amount": 10000,
	"user_id": "ID пользователя"
}'
```

- Транзакции (история)
```shell
curl --request GET \
  --url http://127.0.0.1:8000/user/transactions/ \
  --header 'Authorization: Token ТОКЕН' \
  --header 'Content-Type: application/json'
```

ВАЖНО: приложение запущено в тестовом варианте