# Data Integrator With Flask

## Structure

```
.
├── app/
│   ├── controllers/
│   │   ├── data_management.py
│   │   ├── data_preprocessing.py
│   │   └── file_uploader.py
│   ├── lib/
│   │   ├── preprocessing.py
│   │   └── uploader.py
│   │   └── helper.py
│   ├── static
│   ├── templates
│   ├── __init__.py
│   ├── extensions.py
│   ├── models.py
│   └── register.py
├── run.py
└── settings.py
```

## Penggunaan

1. Setup environment
2. Setup database
3. Install library terdaftar di requirements.txt
4. Buat file .env untuk mendefinisikan keperluan database di settings.py
5. Lalu jalankan ini untuk initialisasi databasenya `flask db init` lalu `flask db migrate -m "initial migration"` dan jangan lupa `flask db upgrade`
5. Jalankan run.py