from dataclasses import dataclass

import pytest
from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework_dataclasses.serializers import DataclassSerializer

from sparkplug_core.utils import get_validated_dataclass


@dataclass
class ExampleDataclass:
    field1: str
    field2: int


class ExampleDataclassSerializer(DataclassSerializer):
    class Meta:
        dataclass = ExampleDataclass


class GetValidatedDataclassTests(TestCase):
    def test_valid_data(self):
        input_data = {"field1": "test", "field2": 123}
        result = get_validated_dataclass(
            serializer_class=ExampleDataclassSerializer,
            input_data=input_data,
        )
        assert isinstance(result, ExampleDataclass)
        assert result.field1 == "test"
        assert result.field2 == 123

    def test_invalid_data(self):
        input_data = {"field1": "test", "field2": "invalid_int"}
        with pytest.raises(ValidationError) as exc_info:
            get_validated_dataclass(
                serializer_class=ExampleDataclassSerializer,
                input_data=input_data,
            )
        assert "field2" in exc_info.value.detail
        assert exc_info.value.detail["field2"][0].code == "invalid"
