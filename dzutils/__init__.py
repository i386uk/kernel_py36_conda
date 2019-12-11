
from .interact import dzform

DZUTILS_DZFORM_MIME_TYPE = 'text/json_dzutils_dzform'

def publish_display_data(*args, **kw):
    # As per bokeh\io\notebook.py v0.12.16
    # This import MUST be deferred or it will introduce a hard dependency on IPython
    from IPython.display import publish_display_data
    return publish_display_data(*args, **kw)

def show_form(name):
    publish_display_data({
        DZUTILS_DZFORM_MIME_TYPE: dzform.get_form_json(name)
    })

