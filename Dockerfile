FROM python:3.8-slim AS builder
ENV DAGSTER_HOME=/opt/dagster/dagster_home/
RUN mkdir -p $DAGSTER_HOME
WORKDIR $DAGSTER_HOME
COPY requirements/ $DAGSTER_HOME/requirements
RUN pip install --no-cache-dir -r $DAGSTER_HOME/requirements/dagster-requirements.txt && \
    groupadd -r dagster && useradd -m -r -g dagster dagster && \
    chown -R dagster:dagster $DAGSTER_HOME
WORKDIR $DAGSTER_HOME

# dagit and daemon
FROM builder AS dagit
EXPOSE 3000
RUN chown -R dagster:dagster $DAGSTER_HOME
USER dagster:dagster
CMD ["dagit", "-h", "0.0.0.0", "--port", "3000", "-w", "workspace.yaml"]

FROM builder AS daemon
USER dagster:dagster
CMD ["dagster-daemon", "run"]

# Compile
FROM python:3.8-slim AS pip-compile
RUN pip install --no-cache-dir pip-tools==6.4.0
COPY . /app

# Formatting
FROM python:3.8-slim AS test
COPY requirements/ $DAGSTER_HOME/requirements
RUN pip install --no-cache-dir -r $DAGSTER_HOME/requirements/dev-requirements.txt
COPY workspaces /src

# workspaces
FROM builder AS data-analytics
COPY workspaces/data_analytics/requirements.txt $DAGSTER_HOME/data-analytics-requirements.txt
RUN pip install --no-cache-dir -r data-analytics-requirements.txt
COPY workspaces/data_analytics/ ./src
WORKDIR $DAGSTER_HOME/src/
USER dagster:dagster
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repo.py"]

FROM builder AS data-analytics-test
COPY workspaces/data_analytics/requirements.txt $DAGSTER_HOME/data-analytics-requirements.txt
RUN pip install --no-cache-dir -r data-analytics-requirements.txt && \
    pip install --no-cache-dir -r $DAGSTER_HOME/requirements/dev-requirements.txt
COPY workspaces/data_analytics/ ./src
WORKDIR $DAGSTER_HOME/src/
USER dagster:dagster
CMD ["python", "-m", "pytest", ".", "-v"]

FROM builder AS data-science
COPY workspaces/data_science/requirements.txt $DAGSTER_HOME/data-science-requirements.txt
RUN pip install --no-cache-dir -r data-science-requirements.txt
COPY workspaces/data_science/ ./src
WORKDIR $DAGSTER_HOME/src/
USER dagster:dagster
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4001", "-f", "repo.py"]

FROM builder AS data-science-test
COPY workspaces/data_science/requirements.txt $DAGSTER_HOME/data-science-requirements.txt
RUN pip install --no-cache-dir -r data-science-requirements.txt && \
    pip install --no-cache-dir -r $DAGSTER_HOME/requirements/dev-requirements.txt
COPY workspaces/data_science/ ./src
WORKDIR $DAGSTER_HOME/src/
USER dagster:dagster
CMD ["python", "-m", "pytest", ".", "-v"]