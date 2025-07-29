from typing import Iterator, List, Set

from .base import Interval, Repeat, Section, ValueSpecification


class ValidationMixin:
    def _iter_content(self, item: Repeat | Section | None = None) -> Iterator[Interval]:
        if item is None:
            item = self

        for item in item.content:
            yield item
            if isinstance(item, (Section, Repeat)):
                yield from self._iter_content(item)
    
    def intervals(self) -> Iterator[Interval]:
        for item in self._iter_content():
            if isinstance(item, Interval):
                yield item

    def repeats(self) -> Iterator[Repeat]:
        for item in self._iter_content():
            if isinstance(item, Repeat):
                yield item
    
    def _get_value_attributes(self, value_specification: ValueSpecification) -> List[str]:
        match value_specification.type:
            case "fixed":
                return ["value"]
            case "range":
                return ["min_value", "max_value"]
            case "ramp":
                return ["start_value", "end_value"]
            case _:
                raise ValueError(f"Unknown value type: {value_specification.type}")
    
    def get_repeat_variables(self) -> Set[str]:
        variables = set()
        for repeat in self.repeats():
            if repeat.count.variable is not None:
                variables.add(repeat.count.variable)

        return variables
    
    def _value_specification_has_default(self, value_specification: ValueSpecification) -> bool:
        attributes = self._get_value_attributes(value_specification)

        match value_specification.type:
            case "range":
                values = [getattr(value_specification, attr) for attr in attributes]
                return any(value is not None for value in values)
            case _:
                return all(getattr(value_specification, attr) is not None for attr in attributes)
    
    def _get_interval_variables(self, interval_attribute: str, ignore_with_default: bool = False) -> Set[str]:
        variables = set()
        for interval in self.intervals():
            volume_or_intensity = getattr(interval, interval_attribute)

            if volume_or_intensity.variable is not None:
                if ignore_with_default and self._value_specification_has_default(volume_or_intensity):
                    continue

                variables.add(volume_or_intensity.variable)

        return variables

    def get_intensity_variables(self, ignore_with_default: bool = False) -> Set[str]:
        return self._get_interval_variables("intensity", ignore_with_default=ignore_with_default)

    def get_volume_variables(self, ignore_with_default: bool = False) -> Set[str]:
        return self._get_interval_variables("volume", ignore_with_default=ignore_with_default)
    
    def get_variables(self) -> Set[str]:
        pass

    def has_only_one_intensity_variable(self, allow_absolute: bool = False) -> bool:
        """
        Check if intensity in the workout is always specified as a variable, and if it is only one variable.
        """
        variables = set()
        
        for interval in self.intervals():
            intensity = interval.intensity

            if intensity.variable is not None:
                variables.add(intensity.variable)
            else:
                if not allow_absolute:
                    return False

        if len(variables) > 1:
            return False
                    
        return True

    def has_only_absolute_intensity(self) -> bool:
        """
        Check if intensity in the workout is always specified as a fixed value, and not as a variable.
        """
        for interval in self.intervals():
            intensity = interval.intensity

            if intensity.variable is not None:
                return False
                    
        return True
    
    def has_only_one_intensity_quantity(self) -> bool:
        """
        Check if intensity in the workout is always specified with the same quantity, and not as a variable.
        """
        quantities = set()

        for interval in self.intervals():
            quantities.add(interval.intensity.quantity)

        if len(quantities) > 1:
            return False

        return True
    
    def has_only_one_volume_quantity(self) -> bool:
        """
        Check if volume in the workout is always specified with the same quantity, and not as a variable.
        """
        quantities = set()

        for interval in self.intervals():
            quantities.add(interval.volume.quantity)

        if len(quantities) > 1:
            return False

        return True
    
    def repeats_are_fixed(self) -> bool:
        """
        Check if repeats are always specified as a fixed value.
        """
        for repeat in self.repeats():
            if repeat.count.type != "fixed" or repeat.count.variable is not None:
                return False
        return True
    
    def volume_is_duration(self) -> bool:
        """
        Check if volume is always specified as duration.
        """
        for interval in self.intervals():
            if interval.volume.quantity != "duration":
                return False
        return True
    
    def intensity_is_power(self) -> bool:
        """
        Check if intensity is always specified as power.
        """
        for interval in self.intervals():
            if interval.intensity.quantity != "power":
                return False
        return True