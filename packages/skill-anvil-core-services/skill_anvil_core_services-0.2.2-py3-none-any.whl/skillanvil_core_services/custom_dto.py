from django.db import models
class DtoModel:
     class Meta:
        abstract = True
     def __init__(self, model_cls):
        if not hasattr(model_cls, "get_available_fields"):
            raise TypeError("model_cls must implement get_available_fields()")
        self.model_cls = model_cls
        

class CustomModel(models.Model):
    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not hasattr(cls, 'get_available_fields') or not callable(getattr(cls, 'get_available_fields')):
            raise TypeError(f"Class '{cls.__name__}' must define a callable 'get_available_fields' method.")

    def get_available_fields_dict(self):
        fields = self.get_available_fields() 
        return {
            field.KEY: field.Value for field in fields
        }