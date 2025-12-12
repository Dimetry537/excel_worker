# excel_worker
# Генерация приватного и публичного ключей для работы системы
```shell
# Generate an RSA private key, of size 2048
openssl genrsa -out jwt-private.pem 2048
```

```shell
# Extract the public key from the key pair, which can be used in a certificate
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
```
# Пароль для Flower
# Генерируем новый пароль
NEW_PASS=$(openssl rand -base64 32)

# Обновляем секрет (nginx и flower подхватят автоматически!)
echo "$NEW_PASS" | docker secret create flower_password_new -
docker secret rm flower_password
docker secret create flower_password flower_password_new
docker secret rm flower_password_new

# Перезапускаем только nginx (остальное работает!)
docker compose -f docker-compose.yml -f docker-compose.prod.yml restart nginx
