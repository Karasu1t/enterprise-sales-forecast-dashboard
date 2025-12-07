FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY train.py ./
RUN pip install pandas scikit-learn joblib pandas-gbq google-cloud-bigquery google-cloud-storage
ENTRYPOINT ["python", "train.py"]
