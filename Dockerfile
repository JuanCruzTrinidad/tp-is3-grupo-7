FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Pre-descarga las stopwords de NLTK en el build para no depender de la red
# en tiempo de ejecución (las hornea en la imagen).
RUN python -c "import nltk; nltk.download('stopwords')"

COPY backend/ .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
