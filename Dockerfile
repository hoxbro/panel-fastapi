FROM mambaorg/micromamba

COPY environment.yml ./
RUN micromamba install -y -n base -f environment.yml
RUN micromamba clean --all --yes

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV BOKEH_RESOURCES cdn
ENV DOCKERENV 1

WORKDIR /app
