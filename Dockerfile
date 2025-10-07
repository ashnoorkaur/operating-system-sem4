FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install pandas matplotlib seaborn
CMD ["python3", "data_analysis.py"]