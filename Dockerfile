FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE  1
ENV PYTHONUNBUFFERED 1

RUN mkdir /E_WalletZ

WORKDIR /E_WalletZ

COPY .  /E_WalletZ/

RUN pip install -r requirements.txt
