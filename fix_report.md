# Internal Dashboard — Звіт по тестовому завданню

## Опис

Було виконано запуск системи за допомогою Docker Compose, проведено аналіз логів, знайдено та виправлено помилки, а також перевірено працездатність сервісів.

## Знайдені проблеми та їх виправлення

### 1. Backend не запускався через відсутню змінну середовища

**Симптом:**
Контейнер `app` завершувався з помилкою (exit code 3).

**Логи:**
KeyError: 'APP_ENV'

**Причина:**
У коді додатку використовується змінна середовища:
ENV = os.environ["APP_ENV"]

Але в `compose.yaml` вона не була визначена (було використано `APP_MODE`).

**Виправлення:**
Змінено:
APP_MODE: dev

на:
APP_ENV: dev

---

### 2. Неправильна точка входу Gunicorn

**Симптом:**
Контейнер `app` завершувався з помилкою.

**Логи:**
Failed to find attribute 'application' in 'main'

**Причина:**
Gunicorn намагався запустити:
main:application

Але у `main.py` об’єкт називається:
app = Flask(**name**)

**Виправлення:**
Змінено:
main:application

на:
main:app

---

### 3. Неправильний порт для backend у Traefik

**Симптом:**
API повертав помилку 502 Bad Gateway.

**Причина:**
Backend працює на порту 8000, але Traefik був налаштований на порт 8080.

**Виправлення:**
Змінено:
traefik.http.services.app.loadbalancer.server.port=8080

на:
traefik.http.services.app.loadbalancer.server.port=8000

---

### 4. Неправильний healthcheck

**Симптом:**
Контейнер міг бути позначений як unhealthy.

**Причина:**
Healthcheck звертався до порту 80 замість 8000.

**Виправлення:**
Змінено:
http://localhost:80/api/health

на:
http://localhost:8000/api/health

---

### 5. Неправильне монтування volume для frontend

**Симптом:**
HTML-сторінка могла не відкриватися.

**Причина:**
Frontend копіює файли у `/out/dist`, але Caddy дивився у неправильний шлях.

**Виправлення:**
Змінено volume:
static:/srv/www/dist

на:
static:/srv/www

та налаштовано Caddy:
root * /srv/www/dist

---

## Команди перевірки працездатності

Запуск системи:
docker compose up --build

Перевірка контейнерів:
docker compose ps

Перевірка логів:
docker compose logs

Перевірка endpoint-ів:
curl -i http://localhost/
curl -i http://localhost/api/
curl -i http://localhost/api/health

---

## Очікуваний результат

http://localhost/ → HTML сторінка
http://localhost/api/ → JSON
http://localhost/api/health → {"status":"OK"}

---

## Висновок

Було знайдено та виправлено критичні помилки конфігурації Docker, середовища виконання та маршрутизації. Після внесення змін система працює відповідно до очікувань.
