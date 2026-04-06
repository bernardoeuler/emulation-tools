FROM python:3.12-slim

WORKDIR /api

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x bin/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./bin/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]