FROM python:3.12.12-slim
LABEL authors="mithilesh"

RUN python -m venv /opt/dev-3.12
ENV PATH="/opt/dev-3.12/bin:$PATH"

RUN groupadd -g 1000 appuser
RUN useradd -m -s /bin/bash -g appuser -u 1000 appuser

ENV API_SERVER_HOST="localhost"
ENV API_SERVER_PORT="8081"
ENV MCP_SERVER_HOST="localhost"
ENV MCP_SERVER_PORT="8080"

COPY requirements.txt .

RUN pip cache purge
RUN mkdir /home/tmp_dir
RUN TMPDIR=/home/tmp_dir pip install --no-cache-dir -r requirements.txt
RUN rm -r /home/tmp_dir
RUN pip cache purge
RUN rm requirements.txt

WORKDIR /app

COPY . .

# Change ownership of app directory and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080 8081

#ENTRYPOINT ["top", "-b"]
