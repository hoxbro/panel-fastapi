# Example of a multipage app with login using FastAPI and Panel

The easiest way to run this example is to use `docker-compose up -d` wait for it to finish and connect to `http://localhost:8080/`. Alternatively, the environment can be installed via `conda`/`mamba` with `mamba env create -n multi -f environment.yml` and run with `uvicorn app.main:app`.

The username and password are both `test`.

If a new panel model has to be added create it in the model folder and add it to `models/__init__.py` like the existing examples.

One of the main focuses of this repo is to easily add a new panel model without changing a lot of code and have a login page to hide the models behind.


### Screenshots
![00 Landing](https://user-images.githubusercontent.com/19758978/154292137-47fb2ee6-dc4b-49b9-8a8e-386131071770.png)
![01 Login](https://user-images.githubusercontent.com/19758978/154292135-a03d38f5-d4bd-4622-8cea-225d58a670c3.png)
![02 App](https://user-images.githubusercontent.com/19758978/154292125-f34c63e3-528d-4c40-b90a-8026da201bd4.png)
