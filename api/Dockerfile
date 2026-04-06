FROM python:3.12-slim

WORKDIR /.temp

RUN apt-get update -y
RUN apt-get dist-upgrade -y
RUN apt-get install -y build-essential cmake git ninja-build p7zip-full unzip zip
RUN rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/CharlesThobe/chdman.git && \
    cd chdman && \
    cmake -B build -G Ninja && \
    cmake --build build && \
    cp build/chdman /usr/local/bin/ && \
    chmod +x /usr/local/bin/chdman

WORKDIR /api

RUN rm -rf /.temp

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x bin/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./bin/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]