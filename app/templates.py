from fastapi.templating import Jinja2Templates


TEMPLATES_DIR = 'app/templates'

templates = Jinja2Templates(directory=TEMPLATES_DIR)
