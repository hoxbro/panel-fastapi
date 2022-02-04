from .button_click import ButtonClick

# Fill out with new models
_models = [
    #  [url, title, model]
    ["buttonclick", "Button Click", ButtonClick],
]

titles = {m[0]: m[1] for m in _models}
serving = {f"/panel/{m[0]}": m[2] for m in _models}
