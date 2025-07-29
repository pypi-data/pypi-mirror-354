from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Generic, List, Literal, Optional, Self, TypeVar, Union
from enum import Enum


class VolumeQuantity(str, Enum):
    duration = "duration"
    distance = "distance"


class IntensityQuantity(str, Enum):
    speed = "speed"
    power = "power"

class RepeatQuantity(str, Enum):
    NUMBER = "number"


QuantityT = TypeVar('QuantityT')


class ValueSpecification(BaseModel, Generic[QuantityT]):
    quantity: QuantityT
    variable: Optional[str] = None


class FixedValue(ValueSpecification):
    type: Literal["fixed"] = "fixed"
    value: Union[int, float, None] = None
    fraction: Optional[float] = None

    @model_validator(mode="after")
    def check_value_or_variable(self) -> Self:
        if self.value is None and self.variable is None:
            raise ValueError("At least one of value or variable must be specified")
        return self

class RangeValue(ValueSpecification):
    type: Literal["range"] = "range"
    min_value: Optional[Union[int, float]] = None
    max_value: Optional[Union[int, float]] = None
    min_fraction: Optional[float] = None
    max_fraction: Optional[float] = None

    @model_validator(mode="after")
    def check_bounded(self) -> Self:
        if self.variable:
            return self
        elif self.min_value is None and self.max_value is None:
            raise ValueError("At least one of min_value, max_value or variable must be specified")
        return self


class RampValue(ValueSpecification):
    type: Literal["ramp"] = "ramp"
    start_value: Optional[Union[int, float]] = None
    end_value: Optional[Union[int, float]] = None
    start_fraction: Optional[float] = None
    end_fraction: Optional[float] = None

    @model_validator(mode="after")
    def check_start_or_end_or_variable(self) -> Self:
        if self.variable:
            if self.start_value is not None or self.end_value is not None:
                raise ValueError("Both start_value and end_value must either be specified or not specified if a variable is specified")
            return self
        elif self.start_value is None and self.end_value is None:
            raise ValueError("Either start_value and end_value or variable must be specified")
        return self

class Instruction(BaseModel):
    type: Literal["instruction"] = "instruction"
    text: str


class Interval(BaseModel):
    type: Literal["interval"] = "interval"
    volume: Union[FixedValue[VolumeQuantity], RangeValue[VolumeQuantity], RampValue[VolumeQuantity]] = Field(..., discriminator="type")
    intensity: Union[FixedValue[IntensityQuantity], RangeValue[IntensityQuantity], RampValue[IntensityQuantity]] = Field(..., discriminator="type")


class Repeat(BaseModel):
    type: Literal["repeat"]
    count: Union[FixedValue[RepeatQuantity], RangeValue[RepeatQuantity]] = Field(..., discriminator="type")
    content: List[Union[Interval, "Repeat", Instruction]]


class Section(BaseModel):
    type: Literal["section"] = "section"
    name: Optional[str]
    content: List[Union[Interval, Repeat, Instruction]]


WorkoutContent = Annotated[
    Union[Interval, Repeat, Section, Instruction],
    Field(discriminator="type")
]


class BaseWorkout(BaseModel):
    title: str | None = None
    description: str | None = None
    content: List[WorkoutContent]

    def model_dump_json(self, *args, **kwargs) -> str:
        """
        Exclude unset fields from the JSON output to keep the format clean.
        """
        kwargs["exclude_unset"] = True
        kwargs["exclude_none"] = True
        return super().model_dump_json(*args, **kwargs)