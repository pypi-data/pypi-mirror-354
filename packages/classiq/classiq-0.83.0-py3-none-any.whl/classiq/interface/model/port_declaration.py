from typing import Any, Literal, Optional

import pydantic
from pydantic_core.core_schema import ValidationInfo

from classiq.interface.exceptions import ClassiqInternalError, ClassiqValueError
from classiq.interface.generator.functions.concrete_types import ConcreteQuantumType
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.functions.type_modifier import (
    TypeModifier,
    TypeQualifier,
)
from classiq.interface.helpers.pydantic_model_helpers import values_with_discriminator
from classiq.interface.model.parameter import Parameter


class AnonPortDeclaration(Parameter):
    quantum_type: ConcreteQuantumType
    direction: PortDeclarationDirection
    type_qualifier: Optional[TypeQualifier] = pydantic.Field(
        default=None, exclude=True
    )  # TODO remove after BWC breaking release https://classiq.atlassian.net/browse/CLS-2777
    kind: Literal["PortDeclaration"]
    type_modifier: TypeModifier = pydantic.Field(default=None)

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_kind(cls, values: Any) -> dict[str, Any]:
        return values_with_discriminator(values, "kind", "PortDeclaration")

    @pydantic.model_validator(mode="before")
    @classmethod
    def _set_type_modifier(cls, values: Any) -> dict[str, Any]:
        if values.get("type_modifier") is None:
            type_qualifier = values.get("type_qualifier")
            if type_qualifier is not None:
                if isinstance(type_qualifier, TypeQualifier):
                    values["type_modifier"] = type_qualifier.to_modifier()
                elif isinstance(type_qualifier, str):
                    values["type_modifier"] = TypeQualifier(
                        type_qualifier
                    ).to_modifier()
                else:
                    raise pydantic.ValidationError("Missing a type modifier")
            else:
                raise pydantic.ValidationError("Missing a type modifier")
        return values

    @pydantic.field_validator("direction", mode="before")
    @classmethod
    def _direction_validator(
        cls, direction: PortDeclarationDirection, info: ValidationInfo
    ) -> PortDeclarationDirection:
        values = info.data
        if direction is PortDeclarationDirection.Output:
            quantum_type = values.get("quantum_type")
            if quantum_type is None:
                raise ClassiqValueError("Port declaration is missing a type")

        return direction

    def rename(self, new_name: str) -> "PortDeclaration":
        if type(self) not in (AnonPortDeclaration, PortDeclaration):
            raise ClassiqInternalError
        return PortDeclaration(**{**self.__dict__, "name": new_name})


class PortDeclaration(AnonPortDeclaration):
    name: str
