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


# Подключаешься по SSH к домену
ssh user@your_domain

# Устанавливаем nginx и утилиты
sudo apt update && sudo apt install nginx openssl htpasswd -y

# Создаём самоподписной сертификат на 10 лет (можно потом заменить на Let’s Encrypt)
sudo mkdir -p /etc/ssl/private /etc/ssl/certs
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:4096 \
  -keyout /etc/ssl/private/internal.key \
  -out /etc/ssl/certs/internal.crt \
  -subj "/CN=YOUR_DOMAIN"

# Создаём пароль для Flower (замени на свой очень сильный)
sudo htpasswd -bc /etc/nginx/.htpasswd_flower admin СуперСекретныйПароль2025

# Создаём конфиг
sudo tee /etc/nginx/sites-available/app <<'EOF'
server {
    listen YOUR_PORT_CERT;
    server_name YOUR_DOMAIN;
    return 301 https://$server_name$request_uri;
}

server {
    listen YOUR_PORT ssl http2;
    server_name YOUR_DOMAIN;

    ssl_certificate     /etc/ssl/certs/internal.crt;
    ssl_certificate_key /etc/ssl/private/internal.key;

    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://your_domain:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /flower/ {
        proxy_pass http://your_domain:5555/;
        proxy_set_header Host $host;
        auth_basic "Flower";
        auth_basic_user_file /etc/nginx/.htpasswd_flower;
    }
}
EOF

# Активируем и перезапускаем
sudo ln -sf /etc/nginx/sites-available/app /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx
