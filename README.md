# Lead Manager

- [Preface](#preface)
- [ER diagram](#er-diagram)
- [Requirements](#requirements)
- [Production](#production)
- [Development](#development)
- [Whats missing](#whats-missing)

## Preface

Regarding the main assignment:

* The assignment specifies `N` subjects and `N` careers, meaning students or 'leads' are taking the same 
amount of classes as careers they are pursuing. I'll assume `Ns (N of subjects) != Nc (N of careers)` as it wouldn't make much sense otherwise. 

* It also defines N as: `[0, N] ^ [N, X]` but `X` is not defined. I'll assume `X = inf`.

Regarding the installation:

This guide assumes you are using ubuntu, debian or some other debian based distribution

## ER diagram

![ER-diagram](./resources/ER-diagram.png)

## Requirements

* [Docker](https://docs.docker.com/engine/install/)

## Production

* Create a .env file in the root directory with the following parameters:
    * `POSTGRES_PASSWORD={YOUR_POSTGRES_PASSWORD}`
    * `PG_HOST=database`

## Development

* Install [python 3.10.12](https://www.python.org/downloads/)
* Create a virtual environment running `python3 -m venv venv`
* Activate virtual environment running `source venv/bin/activate`
* Install requirements with `pip install -r requirements.txt`

* Run application with `uvicorn app:app --forwarded-allow-ips='*' --host 0.0.0.0 --workers 3 --reload`

## API Documentation

For an interactive API documentation you can go to `localhost:8000/docs` (replace localhost for the URL of the server in case you are running it somewhere else)

## Whats missing

* Unit testing for repositories

