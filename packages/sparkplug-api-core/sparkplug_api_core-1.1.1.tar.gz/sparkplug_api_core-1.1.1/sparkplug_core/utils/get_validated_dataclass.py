from dataclasses import dataclass

from rest_framework_dataclasses.serializers import DataclassSerializer


def get_validated_dataclass(
    serializer_class: DataclassSerializer,
    *,
    input_data: dict,
) -> dataclass:
    """Validate serializer input data and return a dataclass."""
    serializer = serializer_class(data=input_data)
    serializer.is_valid(raise_exception=True)

    # Return the validated dataclass instance directly
    return serializer.validated_data
