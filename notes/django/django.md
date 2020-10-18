Django
======

## Dumpdata
```console
python manage.py dumpdata --natural-foreign --natural-primary <app>.<model> -e contenttypes -o users/fixtures/users/users.json
```

## Tips and tricks
### Iterate through model fields:
```python
obj = patients_models.Paciente.objects.get(pk=1)

for field in patients_models.Paciente._meta.get_fields():
    print(field.name, getattr(obj,field.name, None))
```
**Return None when its a reference field. Is empty `""` when the field value
is empty**
