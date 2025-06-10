FROM python:3.11

WORKDIR /app

COPY law_rss_api.py .

RUN pip install flask feedparser

EXPOSE 5000

CMD ["python", "law_rss_api.py"]
