# forgetful_gardner_backend/Dockerfile

FROM python:3.12-slim

RUN apt-get update && \
    apt-get upgrade --yes

RUN useradd --create-home user
USER user
WORKDIR /home/user

ENV VIRTUALENV=/home/user/venv
RUN python3 -m venv $VIRTUALENV
ENV PATH="$VIRTUALENV/bin:$PATH"

COPY --chown=user ./pyproject.toml ./
RUN python -m pip install --upgrade pip setuptools

COPY --chown=user ./src/ src/
RUN python -m pip install .

EXPOSE 8000
CMD ["sh", "src/entrypoint.sh"]