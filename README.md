# 📊 Traffic & Finance Dashboard — Streamlit App

## Що це

Повноцінний аналітичний дашборд для моніторингу KPI трафіку та фінансів iGaming-операцій.

**5 сторінок:**
- 🏠 **Executive Summary** — scorecards, тренди, split analysis, conversion deep dive, country matrix
- 📊 **Daily Operations** — today vs yesterday, daily table, registration methods
- 📈 **Weekly Trends** — volume bars + FTD line, Reg2Dep vs eCPA
- 💳 **Payment Analytics** — approval by method, geo breakdown, chargeback analysis
- 👥 **Agent Performance** — leaderboard, quality vs volume scatter, fraud alerts

**Фічі:**
- 🌙 Dark theme (стиль як у прототипі)
- 🔄 Comparison з попереднім періодом (автоматичний)
- 🎛️ Інтерактивні фільтри: дати, країни, бренди, платформи, джерела
- 🎨 Heatmap у таблицях (зелений → жовтий → червоний)
- ⚡ Alert banner коли Reg2Dep < 10%
- 📊 20+ графіків та таблиць

---

## 🚀 Як задеплоїти за 5 хвилин

### Крок 1: Створи GitHub репозиторій

1. Зайди на **github.com** → натисни **"+"** → **New repository**
2. Назва: `tf-dashboard`
3. Публічний (Public)
4. Натисни **Create repository**

### Крок 2: Завантаж файли

Завантаж ці файли в репозиторій:

```
tf-dashboard/
├── app.py                              ← основний файл додатку
├── requirements.txt                    ← залежності Python
├── TF_Dashboard_Dataset_v2.xlsx        ← датасет
├── .streamlit/
│   └── config.toml                     ← налаштування теми
└── README.md                           ← цей файл
```

**Як завантажити:**
- На сторінці repo натисни **"Add file"** → **"Upload files"**
- Перетягни всі файли
- Натисни **"Commit changes"**

⚠️ Для папки `.streamlit/config.toml`:
- Натисни **"Add file"** → **"Create new file"**
- В полі імені напиши: `.streamlit/config.toml`
- Вставь вміст файлу config.toml
- Commit

### Крок 3: Деплой на Streamlit Cloud

1. Перейди на **share.streamlit.io**
2. Увійди через GitHub
3. Натисни **"New app"**
4. Обери:
   - Repository: `tf-dashboard`
   - Branch: `main`
   - Main file path: `app.py`
5. Натисни **"Deploy!"**
6. Зачекай 2-3 хвилини

### Крок 4: Готово! 🎉

Ти отримаєш URL типу:
```
https://tf-dashboard.streamlit.app
```

Відправ це посилання будь-кому — вони побачать живий дашборд.

---

## 🔧 Як підключити реальні дані

### Варіант А: Замінити Excel файл
1. Експортуй дані з адмінки/ПП у такому ж форматі
2. Замінити файл `TF_Dashboard_Dataset_v2.xlsx` в repo
3. Streamlit автоматично оновиться

### Варіант Б: Підключити BigQuery
Заміни функцію `load_data()` в `app.py` на:

```python
from google.cloud import bigquery
import streamlit as st

@st.cache_data(ttl=3600)
def load_data():
    client = bigquery.Client()
    
    traffic = client.query("""
        SELECT * FROM `project.dataset.daily_traffic`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 MONTH)
    """).to_dataframe()
    
    payments = client.query("""
        SELECT * FROM `project.dataset.payments`
        WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 MONTH)
    """).to_dataframe()
    
    # ... аналогічно для інших таблиць
    
    return traffic, payments, agents, geo_dim
```

Додай в `requirements.txt`:
```
google-cloud-bigquery>=3.0.0
db-dtypes>=1.0.0
```

І в Streamlit Cloud → Settings → Secrets додай JSON ключ сервісного аккаунта.

### Варіант В: Google Sheets (live)
```python
import gspread
from google.oauth2.service_account import Credentials

@st.cache_data(ttl=600)  # Оновлювати кожні 10 хв
def load_data():
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    gc = gspread.authorize(creds)
    sh = gc.open("TF_Dashboard_Data_Source")
    traffic = pd.DataFrame(sh.worksheet("FACT_Daily_Traffic").get_all_records())
    # ...
```

---

## 📝 Кастомізація

### Змінити кольори
В `app.py` знайди блок `COLORS` і зміни:
```python
COLORS = {
    'blue': '#5B8DEF',    # Основний акцент
    'green': '#3DDFA0',   # Позитивні зміни
    'red': '#F06A6A',     # Негативні зміни
    ...
}
```

### Додати нову метрику
1. Додай calculated field в словник `compute_kpis()`
2. Додай scorecard або KPI pill в відповідну секцію

### Змінити порогові значення алертів
Знайди `if kpi['reg2dep'] < 0.10:` і зміни `0.10` на потрібне значення.

---

## 📋 Структура датасету

| Лист | Рядків | Опис |
|------|--------|------|
| FACT_Daily_Traffic | ~12,000 | Основна факт-таблиця |
| FACT_Payments | ~6,600 | Деталізація платіжних методів |
| FACT_Agent_Weekly | ~2,300 | Перформанс агентів |
| DIM_Geo | 8 | Довідник країн |
| DIM_KPI_Targets | 8 | Цільові значення |
| META_Calculated_Fields | 17 | Формули для розрахунків |
| META_Data_Dictionary | 30 | Опис кожного поля |
