FROM python:3.12.12-slim
LABEL authors="mithi_w"

RUN python -m venv /opt/dev-3.12
ENV PATH="/opt/dev-3.12/bin:$PATH"

RUN groupadd -g 1000 appuser
RUN useradd -m -s /bin/bash -u 1000 -g appuser appuser

WORKDIR /app

RUN export PYTHONPATH=.:$PYTHONPATH

ENV API_SERVER_HOST="localhost"
ENV API_SERVER_PORT="8081"
ENV MCP_SERVER_HOST="localhost"
ENV MCP_SERVER_PORT="8080"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Change ownership of app directory and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080 8081

#ENTRYPOINT ["top", "-b"]