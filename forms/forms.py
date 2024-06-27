from .form import BaseFormWidget


class OutflowsForm(BaseFormWidget):
    """A form widget for managing Outflows"""
    FORM_FIELDS = (
        ('title', 'title_field'),
        ('value', 'value_field'),
        ('date', 'date_field'),
        ('prediction', 'checkbox_field'),
        ('notes', 'notes_field'),
    )
    REQUIRED_FIELDS = ('title', 'value', 'date')


class InflowsForm(BaseFormWidget):
    """A form widget for managing Inflows"""
    FORM_FIELDS = (
        ('title', 'title_field'),
        ('value', 'value_field'),
        ('date', 'date_field'),
        ('notes', 'notes_field'),
    )
    REQUIRED_FIELDS = ('title', 'value', 'date')
