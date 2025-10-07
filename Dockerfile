FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install pandas matplotlib seaborn
RUN pip install azure-storage-blob 
RUN pip install python-dotenv
CMD ["python3", "data_analysis.py"]
