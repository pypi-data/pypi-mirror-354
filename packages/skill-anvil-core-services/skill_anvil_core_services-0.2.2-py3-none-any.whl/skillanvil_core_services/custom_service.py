# core_services/services/custom_service.py

from typing import  Any
from rest_framework import serializers
from rest_framework import status
from rest_framework.exceptions import ValidationError
from typing import TypeVar, Type, Generic
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError
from typing import TypeVar, Type, Generic

T = TypeVar("T")

class CustomSerializerRequest(serializers.Serializer, Generic[T]):
    @classmethod
    def validate_and_retrieve_data_or_throw_exception(cls: Type['CustomSerializerRequest'], data) -> T:
        serializer_instance = cls(data=data)
        if serializer_instance.is_valid():
            try:
                model_cls = cls.Meta.model
            except AttributeError:
                raise RuntimeError("Meta.model is not defined in the serializer.")
            return model_cls(**serializer_instance.validated_data)
        else:
            raise ValidationError(detail=serializer_instance.errors, code=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def retrieve_instance(cls: Type['CustomSerializerRequest'], data) -> T:
        serializer_instance = cls(data=data)
        serializer_instance.is_valid(raise_exception=True)
        try:
            model_cls = cls.Meta.model
        except AttributeError:
            raise RuntimeError("Meta.model is not defined in the serializer.")
        return model_cls(**serializer_instance.validated_data)
class CustomService:
    def __init__(self, serializer):
       if not issubclass(serializer, CustomSerializerRequest):
            raise TypeError(
                f"Serializer must inherit from CustomSerializerRequest, got {serializer.__name__}"
            )
       self.serializer = serializer

    def get_object(self, pk, serialized=False):
        instance = self.serializer.Meta.model.objects.get(pk=pk)
        return self.serializer(instance).data if serialized else instance

    def get_all_objects(self, serialized=False):
        instances = self.serializer.Meta.model.objects.all()
        return self.serializer(instances, many=True).data if serialized else instances

    def get_objects_with_id_in_list(self, ids: list, serialized=False):
        instances = self.serializer.Meta.model.objects.filter(pk__in=ids)
        return self.serializer(instances, many=True).data if serialized else instances

    def create_object_or_raise_exception(self, data: Any, raise_exception=True):
        serializer_instance = self.serializer(data=data)
        serializer_instance.is_valid(raise_exception=raise_exception)
        return serializer_instance.save()

    def update_object(self, data: Any):
        instance = self.serializer.Meta.model.objects.get(pk=data['id'])
        serializer_instance = self.serializer(instance, data=data)
        serializer_instance.is_valid(raise_exception=True)
        return serializer_instance.save()

    def delete_object(self, pk):
        return self.serializer.raise_exception_if_not_valid_or_delete_data(
            raise_exception=True, pk=pk
        )


class CustomModelSerializer(serializers.ModelSerializer):
    def custom_validate(self, attrs):
        response = super().validate(attrs)
        if not response.is_valid():  
            raise Exception(response.errors, status=status.HTTP_400_BAD_REQUEST)
        return response
    
    def _method(self, raise_exception=True, update_instance=False, create_instance=False,return_entitie=False):
        if self.is_valid():
            if update_instance:
                self.save()
                return True
            elif create_instance:
                instance = self.save()
                if return_entitie:
                    return instance
                else:
                    return True
        elif raise_exception:
            raise Exception(self.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return None

    def raise_exception_if_not_valid(self, raise_exception=True):
        return self._method(raise_exception=raise_exception)
    
    def raise_exception_if_not_valid_or_update_data(self, raise_exception=True):
        return self._method(raise_exception=raise_exception, update_instance=True)

    def raise_exception_if_not_valid_or_create_data(self, raise_exception=True,return_entitie=False):
        #DESCRIPTION 
        return self._method(raise_exception=raise_exception, create_instance=True,return_entitie=return_entitie)
    @classmethod
    def many_init(cls, *args, **kwargs):
        class _CustomListSerializer(serializers.ListSerializer):
            def raise_exception_if_not_valid_or_create_data_many(self, raise_exception=True, return_entitie=False):
                if self.is_valid():
                    instances = self.save()
                    if return_entitie:
                        return instances
                    else:
                        ids = [instance.id for instance in instances]
                        return True
                elif raise_exception:
                    raise Exception(self.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return None

        kwargs['child'] = cls()
        return _CustomListSerializer(*args, **kwargs)

    @classmethod
    def raise_exception_if_not_valid_or_delete_data(cls,raise_exception=True,instance=None,pk=None):
        if instance is not None:
            instance.delete()
            return True
        elif pk is not None:
            cls.Meta.model.objects.get(id=pk).delete()
            return True
        else:
            raise Exception("instance or pk must be provided")
        
        
        
        
        
        
        
        
        
        
        
        
        
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