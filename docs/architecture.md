# Архитектура

```mermaid
flowchart LR
    User[Пользователь в браузере] --> UI[Streamlit UI]
    UI --> Analytics[Функции аналитики / pandas]
    UI --> Data[SQLAlchemy ORM]
    Data --> DB[(PostgreSQL 16 в Docker Compose)]
    Analytics --> Charts[Plotly графики]
    Charts --> UI
```

## Компоненты
- `src/main.py`: формы, фильтры, графики и интерфейс.
- `src/services/database.py`: модель операций и CRUD.
- `src/utils/analytics.py`: агрегирование показателей.
- `tests/`: автоматизированные тесты.

PostgreSQL запускается через Docker Compose, приложение локально через Streamlit.
