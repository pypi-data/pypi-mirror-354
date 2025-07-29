from typing import List, Self

from .validation import ValidationMixin
from .base import BaseWorkout, FixedValue, Instruction, Interval, RampValue, RangeValue, Repeat, Section


class Workout(BaseWorkout, ValidationMixin):
    def _range_to_mean(self, item: Interval) -> Interval:
        if isinstance(item.volume, RangeValue):
            item.volume = FixedValue(
                value=(item.volume.min_value + item.volume.max_value) / 2,
                quantity=item.volume.quantity
            )

        if isinstance(item.intensity, RangeValue):
            item.intensity = FixedValue(
                value=(item.intensity.min_value + item.intensity.max_value) / 2,
                quantity=item.intensity.quantity
            )

        return item

    def _flatten_item(self, item, *, repeat_count=1, range_to_mean: bool = False) -> List[Interval]:
        if isinstance(item, Interval):
            if range_to_mean:
                return [self._range_to_mean(item)] * repeat_count
            else:
                return [item] * repeat_count
        elif isinstance(item, Repeat):
            # Get the count value, assuming it's a fixed value for now
            count = item.count.value if isinstance(item.count, FixedValue) else 1
            flattened = []
            # Repeat the sequence count times
            for _ in range(count):
                for content_item in item.content:
                    if not isinstance(content_item, Instruction):
                        flattened.extend(self._flatten_item(content_item, repeat_count=1, range_to_mean=range_to_mean))
            return flattened
        elif isinstance(item, Section):
            flattened = []
            for content_item in item.content:
                if not isinstance(content_item, Instruction):
                    flattened.extend(self._flatten_item(content_item, repeat_count=1, range_to_mean=range_to_mean))
            return flattened
        return []

    def flattened_intervals(self, range_to_mean: bool = False) -> Self:
        """Recursively flatten the workout into a list of intervals."""

        intervals = []
        for item in self.content:
            if not isinstance(item, Instruction):
                intervals.extend(self._flatten_item(item, range_to_mean=range_to_mean))
        return intervals

Repeat.model_rebuild()
Section.model_rebuild()