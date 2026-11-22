# Analytics Dashboard

Учебный проект по дисциплине «Современные технологии программирования».

**Тип №3:** сервис обработки и визуализации данных. Интерактивный учёт доходов и расходов с PostgreSQL, Streamlit и Plotly.

## Возможности
- Добавление и удаление операций
- Графики доходов/расходов по месяцам и расходов по категориям
- Фильтрация по датам и категориям
- KPI: доходы, расходы, баланс
- Демо-данные по кнопке (только если таблица пуста)

## Запуск
Установите Docker Desktop и Python 3.11+.

```bash
cp .env.example .env
docker compose up -d --wait
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run src/main.py
```

Откройте http://localhost:8501. Для проверки БД: `docker compose ps`.

## Тесты
```bash
pytest -q
```

## Видео

[▶ Посмотреть видеодемонстрацию приложения](docs/demo.mp4)

Короткая демонстрация работы Analytics Dashboard: финансовые показатели, графики и добавление операции.

## Стек
Python, Streamlit, Plotly, SQLAlchemy, psycopg, PostgreSQL 16, Docker Compose, pytest.

## Архитектура
См. [docs/architecture.md](docs/architecture.md).

## Замечания
Это учебный проект без регистрации и многопользовательской изоляции. Для публичного размещения потребуются авторизация, миграции и усиление безопасности. Не загружайте `.env` в GitHub.
