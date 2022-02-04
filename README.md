# Example of a multipage app with login using FastAPI and Panel

The easiest way to run this example is to use `docker-compose up -d` wait for it to finish and connect to `http://localhost:8080/`. Alternatively, the environment can be installed via `conda`/`mamba` with `mamba env create -n multi -f environment.yml` and run with `uvicorn app.main:app`.

The username and password are both `test`.

If a new panel model has to be added create it in the model folder and add it to `models/__init__.py` like the existing examples.

One of the main focuses of this repo is to easily add a new panel model without changing a lot of unnecessary code and have a login page to hide the models behind.
