import json
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from collections import defaultdict, deque
from dataclasses import MISSING
from dataclasses import field as dataclass_field
from dataclasses import fields, make_dataclass
from enum import Enum
from typing import Any, Deque, Dict, List, Set, get_args

from vajra.config.base_poly_config import BasePolyConfig
from vajra.config.utils import (
    get_all_subclasses,
    get_inner_type,
    is_composed_of_primitives,
    is_dict,
    is_list,
    is_optional,
    is_primitive_type,
    is_subclass,
    to_snake_case,
)


def topological_sort(dataclass_dependencies: Dict[Any, Set[Any]]) -> List[Any]:
    in_degree: Dict[Any, int] = defaultdict(int)
    for cls, dependencies in dataclass_dependencies.items():
        # Ensure every class is present in in_degree
        if cls not in in_degree:
            in_degree[cls] = 0
        for dep in dependencies:
            in_degree[dep] += 1

    zero_in_degree_classes: Deque[Any] = deque(
        [cls for cls in in_degree if in_degree[cls] == 0]
    )
    sorted_classes: List[Any] = []

    while zero_in_degree_classes:
        cls = zero_in_degree_classes.popleft()
        sorted_classes.append(cls)
        for dep in dataclass_dependencies[cls]:
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                zero_in_degree_classes.append(dep)
    return sorted_classes


def _reconstruct_original_dataclass(self) -> Any:
    """
    This function is dynamically mapped to FlatClass as an instance method.
    """
    sorted_classes = topological_sort(self.dataclass_dependencies)
    instances: Dict[Any, Any] = {}

    for _cls in reversed(sorted_classes):
        args: Dict[str, Any] = {}

        for prefixed_field_name, original_field_name, field_type in self.dataclass_args[
            _cls
        ]:
            if is_subclass(field_type, BasePolyConfig):

                config_type_name = getattr(self, f"{original_field_name}_type")

                if isinstance(config_type_name, str):
                    config_type_name = config_type_name.strip('"').upper()
                else:
                    if isinstance(config_type_name, Enum):
                        config_type_name = config_type_name.value.upper()
                    else:
                        config_type_name = config_type_name.name.upper()

                # find all subclasses of field_type and check which one matches the config_type_name
                for subclass in get_all_subclasses(field_type):
                    subclass_type_name = subclass.get_type()
                    if isinstance(subclass_type_name, Enum):
                        subclass_type_name = subclass_type_name.value.upper()
                    else:
                        subclass_type_name = subclass_type_name.name.upper()
                    if subclass_type_name == config_type_name:
                        args[original_field_name] = instances[subclass]
                        break
            elif hasattr(field_type, "__dataclass_fields__"):
                args[original_field_name] = instances[field_type]
            else:
                args[original_field_name] = getattr(self, prefixed_field_name)

        instances[_cls] = _cls(**args)

    return instances[sorted_classes[0]]


def _create_from_cli_args(cls) -> Any:
    """
    This function is dynamically mapped to FlatClass as a class method.
    """
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    for field in fields(cls):
        nargs = None
        field_type = field.type
        help_text = field.metadata.get("help", None)

        if is_optional(field.type):  # type: ignore
            field_type = get_inner_type(field.type)  # type: ignore

        if is_list(field_type):  # type: ignore
            assert is_composed_of_primitives(field_type)  # type: ignore
            field_type = get_args(field_type)[0]
            if is_primitive_type(field_type):
                nargs = "+"
            else:
                field_type = json.loads
        elif is_dict(field_type):  # type: ignore
            assert is_composed_of_primitives(field_type)  # type: ignore
            field_type = json.loads
        elif field_type == bool:
            field_type = lambda x: x.lower() == "true"

        # handle cases with default and default factory args
        if field.metadata.get("type") == "Enum":
            parser.add_argument(
                f"--{field.name}",
                type=field_type,
                choices=field.metadata["choices"],
                default=field.default,
                nargs=nargs,
                help=help_text,
            )
        elif field.metadata.get("type") == "Pybind11Enum":
            parser.add_argument(
                f"--{field.name}",
                type=field_type,
                choices=field.metadata["choices"],
                default=field.default,
                nargs=nargs,
                help=help_text,
            )
        elif field.default is not MISSING:
            parser.add_argument(
                f"--{field.name}",
                type=field_type,
                default=field.default,
                nargs=nargs,
                help=help_text,
            )
        elif field.default_factory is not MISSING:
            parser.add_argument(
                f"--{field.name}",
                type=field_type,
                default=field.default_factory(),
                nargs=nargs,
                help=help_text,
            )
        else:
            parser.add_argument(
                f"--{field.name}",
                type=field_type,
                required=True,
                nargs=nargs,
                help=help_text,
            )

    args = parser.parse_args()

    return cls(**vars(args))


def get_config_class_by_type_name(config_class: Any, type_name: str) -> Any:
    for subclass in get_all_subclasses(config_class):
        if subclass.get_type().value == type_name:
            return subclass

    raise ValueError(f"Config class with name {type_name} not found.")


def create_flat_dataclass(input_dataclass: Any) -> Any:
    """
    Creates a new FlatClass type by recursively flattening the input dataclass.
    This allows for easy parsing of command line arguments along with storing/loading the configuration to/from a file.
    """
    meta_fields = []
    processed_classes = set()
    dataclass_args = defaultdict(list)
    dataclass_dependencies = defaultdict(set)

    def process_dataclass(_input_dataclass: Any, prefix=""):
        if _input_dataclass in processed_classes:
            return

        processed_classes.add(_input_dataclass)

        for field in fields(_input_dataclass):
            prefixed_name = f"{prefix}{field.name}"

            if isinstance(field.type, type) and is_optional(field.type):
                inner = get_inner_type(field.type)
                field_type = inner
            else:
                field_type = field.type

            # # if field is a BasePolyConfig, add a type argument and process it as a dataclass
            if is_subclass(field_type, BasePolyConfig):
                dataclass_args[_input_dataclass].append(
                    (field.name, field.name, field_type)
                )

                type_field_name = f"{field.name}_type"
                assert field.default_factory is not MISSING
                default_value = field.default_factory().get_type()

                metadata = field.metadata.copy()
                if isinstance(default_value, Enum):
                    metadata["type"] = "Enum"
                    metadata["choices"] = [
                        choice.value.upper()
                        for choice in type(default_value).__members__.values()
                    ]
                    default_value = default_value.value.upper()
                else:
                    metadata["type"] = "Pybind11Enum"
                    metadata["choices"] = [
                        choice for choice in type(default_value).__members__.keys()
                    ]
                    default_value = default_value.name.upper()

                meta_fields.append(
                    (
                        type_field_name,
                        type(default_value),
                        dataclass_field(default=default_value, metadata=metadata),
                    )
                )

                assert hasattr(field_type, "__dataclass_fields__")
                for subclass in get_all_subclasses(field_type):
                    dataclass_dependencies[_input_dataclass].add(subclass)
                    process_dataclass(subclass, f"{to_snake_case(subclass.__name__)}_")
                continue

            # if field is a dataclass, recursively process it
            if hasattr(field_type, "__dataclass_fields__"):
                dataclass_dependencies[_input_dataclass].add(field_type)
                dataclass_args[_input_dataclass].append(
                    (field.name, field.name, field_type)
                )
                process_dataclass(field_type, f"{to_snake_case(field_type.__name__)}_")  # type: ignore
                continue

            # Normal field: keep default or default factory if any
            field_default = field.default if field.default is not MISSING else MISSING
            field_default_factory = (
                field.default_factory
                if field.default_factory is not MISSING
                else MISSING
            )

            if field_default is not MISSING:
                meta_fields.append(
                    (
                        prefixed_name,
                        field_type,
                        dataclass_field(default=field.default, metadata=field.metadata),
                    )
                )
            elif field_default_factory is not MISSING:
                meta_fields.append(
                    (
                        prefixed_name,
                        field_type,
                        dataclass_field(
                            default_factory=field.default_factory,
                            metadata=field.metadata,
                        ),
                    )
                )
            else:
                meta_fields.append(
                    (
                        prefixed_name,
                        field_type,
                        dataclass_field(metadata=field.metadata),
                    )
                )

            dataclass_args[_input_dataclass].append(
                (prefixed_name, field.name, field_type)
            )

    process_dataclass(input_dataclass)

    # Sort fields to ensure non-default args come first
    sorted_meta_fields = sorted(meta_fields, key=lambda x: x[2].default is not MISSING)

    FlatClass = make_dataclass("FlatClass", sorted_meta_fields)

    setattr(FlatClass, "dataclass_args", dataclass_args)
    setattr(FlatClass, "dataclass_dependencies", dataclass_dependencies)
    setattr(
        FlatClass, "reconstruct_original_dataclass", _reconstruct_original_dataclass
    )
    setattr(FlatClass, "create_from_cli_args", classmethod(_create_from_cli_args))

    return FlatClass
