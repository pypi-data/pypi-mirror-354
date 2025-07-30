# Django UUID7

A Django package that provides UUID7 field support for PostgreSQL, MariaDB, and MySQL databases.

## Features

- UUID7 field type for Django models
- UUID7 serializer field for Django REST Framework
- UUID7 form field for Django forms
- Support for PostgreSQL, MariaDB, and MySQL databases
- Standalone UUID7 functionality

## Installation

```bash
pip install django-uuid7
```

## Usage

### Model Field

```python
from django.db import models
from django_uuid7 import UUID7Field

class MyModel(models.Model):
    id = UUID7Field(primary_key=True)
    # ... other fields
```

### Serializer Field

```python
from rest_framework import serializers
from django_uuid7 import UUID7SerializerField

class MySerializer(serializers.ModelSerializer):
    id = UUID7SerializerField()
    
    class Meta:
        model = MyModel
        fields = ['id', ...]
```

### Form Field

```python
from django import forms
from django_uuid7 import UUID7FormField

class MyForm(forms.Form):
    id = UUID7FormField()
```

### Standalone Usage

```python
from django_uuid7 import uuid7

# Generate a new UUID7
new_uuid = uuid7()
```

## Requirements

- Python 3.8+
- Django 3.2+
- PostgreSQL, MariaDB, or MySQL database

## License

MIT License 