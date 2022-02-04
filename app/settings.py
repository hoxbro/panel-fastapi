from fastapi.templating import Jinja2Templates

from models import titles

__version__ = "0.1.0"

templates = Jinja2Templates(directory="templates")

GLOBAL_CONTEXT = {"version": __version__, "titles": titles}

SECRET_KEY = "CHANGEMEFORTHELOVEOFGOD!!!!!!!!!"

ALLOWED_HOSTS = ["*"]  # Could be made more specific
