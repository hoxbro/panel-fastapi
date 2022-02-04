import panel as pn
import param


class ButtonClick(pn.viewable.Viewer):
    def __init__(self, **params):
        self.button = pn.widgets.Button(name="Click")
        super().__init__(**params)

    @param.depends("button.clicks")
    def _update_button_click(self):
        return pn.pane.Markdown(f"# {self.button.clicks}")

    def __panel__(self):
        return pn.Column(self.button, self._update_button_click)


if __name__ == "__main__":
    app = ButtonClick()
    app.show(port=5007)
elif __name__.startswith("bokeh"):
    app = ButtonClick()
    app.servable()
