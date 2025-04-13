FROM python:3.12-slim-bookworm

WORKDIR /app

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8501

ENV FLASK_ENV=production

CMD ["streamlit", "run", "app.py", "--server.port=8501"]