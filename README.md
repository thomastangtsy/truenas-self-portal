# TrueNAS Self-Portal

> ### ⚠ Warning ⚠
>
> This is a prototype and it is not garanteed to work at all time.

## Prerequisite

- [Python 3.8](https://www.python.org/)
- (Optional) [venv module](https://docs.python.org/3/library/venv.html) or [virtualenv](https://virtualenv.pypa.io/)
- API key from TrueNAS SCALE

## Quick start

1. Copy `.env.example` to `.env` and modify the environment variables.
2. Build Docker image and run.
   ```sh
   docker build -t truenas-self-portal:latest
   docker run --rm -it truenas-self-portal:latest
   ```
