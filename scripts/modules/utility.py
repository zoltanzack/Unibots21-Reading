import ipywidgets as widgets

style = {'description_width': 'initial'}

def createPinField(initial_value, description, min, max):
    return widgets.BoundedIntText(
        value=initial_value,
        description=description,
        style=style,
        min=min, max=max,
        disabled=False
    )

def createIntSliderField(initial_value, description, min, max):
    return widgets.IntSlider(
        value=initial_value,
        description=description,
        style=style,
        min=min, max=max,
        disabled=False
    )

def createDropdownField(options, initial_value, description):
    return widgets.Dropdown(
        options=options,
        value=initial_value,
        description=description,
        disabled=False,
    )