# Flight Delay Prediction - MLOps CI/CD Pipeline

Bu proje, uçak gecikme tahmini için bir MLOps CI/CD altyapısı içermektedir.

## Proje Yapısı

```
flight-delay-cicd/
├── .github/workflows/mlops_pipeline.yml  # GitHub Actions CI/CD Config
├── src/
│   ├── features.py      # Hashing ve Bucketing fonksiyonları
│   ├── model.py         # Keras Model class'ı
│   └── app.py           # FastAPI ile Stateless Serving Endpoint'i
├── tests/
│   ├── test_unit.py     # Pytest: Hashing mantığını test et
│   └── test_integration.py # Pytest: Model prediction akışını test et
├── Dockerfile           # Uygulamayı paketlemek için
├── requirements.txt     # Python dependencies
└── smoke_test.sh        # Container çalışırken endpoint test scripti
```

## Kurulum

### Yerel Geliştirme

1. Python 3.9 yüklü olduğundan emin olun
2. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

### Docker ile Çalıştırma

1. Docker image'ı oluşturun:
```bash
docker build -t flight-delay-prediction:latest .
```

2. Container'ı çalıştırın:
```bash
docker run -p 8000:8000 flight-delay-prediction:latest
```

3. Smoke test çalıştırın:
```bash
chmod +x smoke_test.sh
./smoke_test.sh
```

## API Endpoints

### GET /
Root endpoint - API bilgilerini döner

### GET /health
Health check endpoint

### POST /predict
Uçak gecikme tahmini yapar

**Request Body:**
```json
{
  "airport_code": "JFK"
}
```

**Response:**
```json
{
  "airport_code": "JFK",
  "predicted_delay_minutes": 25.5,
  "delay_category": 1
}
```

## Testler

### Unit Testler
```bash
pytest tests/test_unit.py -v
```

### Integration Testler
```bash
pytest tests/test_integration.py -v
```

### Tüm Testler
```bash
pytest tests/ -v
```

## CI/CD Pipeline

GitHub Actions workflow şu adımları içerir:
1. Code checkout
2. Dependency installation
3. Linting (pylint)
4. Unit tests
5. Integration tests
6. Docker image build
7. Container run ve smoke test

Pipeline, `main`, `master` veya `develop` branch'lerine push veya PR açıldığında otomatik çalışır.

