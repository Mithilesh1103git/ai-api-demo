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

ENV TMPDIR_PATH="/home/tmp_dir"

RUN mkdir $TMPDIR_PATH

RUN export TMPDIR=$TMPDIR_PATH

ENV PIP_REQ_FILE="requirements.txt"

COPY $PIP_REQ_FILE requirements.txt

RUN python3 -m pip install --upgrade pip
RUN pip cache purge
RUN TMPDIR=$TMPDIR_PATH pip install --no-cache-dir -r requirements.txt
RUN rm -r requirements.txt
RUN pip cache purge

RUN chmod -R -x $TMPDIR_PATH

RUN chmod a-x $TMPDIR_PATH

#---------------------------------------------------------------

WORKDIR /app

COPY . .

# Change ownership of app directory and switch to non-root user
RUN chown -R appuser:appuser /app

RUN usermod -rG sudo appuser

USER appuser

EXPOSE 8080/tcp 8081/tcp
