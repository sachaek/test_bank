from typing import Any, get_type_hints, get_origin, Annotated


class ModelGenerator:
    @staticmethod
    def generate(cls: type) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name, annotated_type in type_hints.items():
            rule = None
            actual_type = annotated_type()

            if get_origin(annotated_type) is Annotated: