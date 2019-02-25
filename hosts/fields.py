import re

from django.db import models
from django import forms


class ModbusAddressFormField(forms.CharField):
    default_error_messages = {
        'invalid': 'Enter a valid Hexadecimal Modbus address: e.g. "4000A"',
    }

    def clean(self, value):
        print("clean")
        if (not (value == '' and not self.required) and
                not re.match('^[A-Fa-f0-9]+$', value) ):
            raise forms.ValidationError(self.error_messages['invalid'])
        print(value)
        return value


class ModbusAddress(models.CharField):
    """
    Field to store hex values.

    On Database side an integerfield is used.
    """
    # TODO: Use same sort of BigPositiveIntegerField
    description = "Saves a hex value into an charfield"

    def to_python(self, value):
        if isinstance(value, str) :
            hex_value = value.upper()
        elif value is None:
            hex_value = value
            
        return hex_value
    
    def formfield(self, **kwargs):
        defaults = {'form_class': ModbusAddressFormField}
        defaults.update(kwargs)
        return super().formfield(**defaults)