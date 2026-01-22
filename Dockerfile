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

#---------------------------------------------------------------
# python packages installation with pip

ENV PIP_TMPDIR_PATH="/home/tmp_dir"
ENV PIP_REQ_FILE="requirements.txt"

COPY $PIP_REQ_FILE requirements.txt

RUN pip cache purge
RUN mkdir $PIP_TMPDIR_PATH
RUN TMPDIR=$PIP_TMPDIR_PATH pip install --no-cache-dir -r requirements.txt
RUN rm -r requirements.txt
RUN pip cache purge+

RUN rm requirements.txt

#---------------------------------------------------------------

WORKDIR /app

COPY . .

# Change ownership of app directory and switch to non-root user
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8080/tcp 8081/tcp

#ENTRYPOINT ["top", "-b"]
