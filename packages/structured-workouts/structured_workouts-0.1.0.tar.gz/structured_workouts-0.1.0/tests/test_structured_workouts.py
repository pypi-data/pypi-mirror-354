import pytest
from pydantic import ValidationError

from structured_workouts.schema import Workout


def test_various():
    with open("tests/test-data/various.json", "r") as f:
        workout = Workout.model_validate_json(f.read())
    
    assert workout.title == "Workout A"

    assert workout.content[0].type == "interval"
    assert workout.content[0].volume.quantity == "duration"
    assert workout.content[0].intensity.quantity == "power"

    assert workout.content[1].type == "repeat"
    assert workout.content[1].count.value == 3
    assert workout.content[1].count.type == "fixed"
    assert workout.content[1].count.quantity == "number"
    assert workout.content[1].content[0].type == "instruction"
    assert workout.content[1].content[0].text == "Don't push too hard"
    assert workout.content[1].content[1].type == "interval"
    assert workout.content[1].content[1].volume.quantity == "distance"
    assert workout.content[1].content[1].intensity.type == "ramp"
    assert workout.content[1].content[1].intensity.quantity == "speed"

    assert workout.content[2].type == "section"
    assert workout.content[2].name == "Cool Down"
    assert workout.content[2].content[0].type == "interval"
    assert workout.content[2].content[0].volume.quantity == "duration"
    assert workout.content[2].content[0].intensity.type == "range"
    assert workout.content[2].content[0].intensity.quantity == "speed"
    assert workout.content[2].content[0].intensity.max_value == 5.0


def test_fixed_range_ramp():
    with open("tests/test-data/fixed-range-ramp.json", "r") as f:
        workout = Workout.model_validate_json(f.read())
    
    assert workout.title == "Workout with fixed range ramp"

    assert workout.content[0].type == "interval"
    assert workout.content[0].volume.quantity == "duration"
    assert workout.content[0].volume.type == "fixed"
    assert workout.content[0].intensity.quantity == "power"
    assert workout.content[0].intensity.type == "range"

    assert workout.content[1].type == "interval"
    assert workout.content[1].volume.type == "fixed"
    assert workout.content[1].volume.quantity == "distance"
    assert workout.content[1].intensity.quantity == "power"
    assert workout.content[1].intensity.type == "ramp"


def test_error_volume_quantity():
    with open("tests/test-data/error-volume-quantity.json", "r") as f:
        with pytest.raises(ValidationError):
            Workout.model_validate_json(f.read())


def test_section():
    with open("tests/test-data/section.json", "r") as f:
        workout = Workout.model_validate_json(f.read())
    
    assert workout.title == "Workout with section"
    assert workout.content[0].type == "section"
    assert workout.content[0].name == "Warm Up"
    assert workout.content[0].content[0].type == "interval"


def test_instruction():
    with open("tests/test-data/instruction.json", "r") as f:
        workout = Workout.model_validate_json(f.read())
    
    assert workout.title == "Workout with instruction"
    assert workout.content[0].type == "instruction"
    assert workout.content[0].text == "Don't push too hard"


def test_repeat():
    with open("tests/test-data/repeat.json", "r") as f:
        workout = Workout.model_validate_json(f.read())
    
    assert workout.title == "Workout with repeat"
    assert workout.content[0].type == "repeat"
    assert workout.content[0].count.quantity == "number"
    assert workout.content[0].count.type == "fixed"
    assert workout.content[0].count.value == 3
    assert len(workout.content[0].content) == 0


def test_variable():
    with open("tests/test-data/variable.json", "r") as f:
        workout = Workout.model_validate_json(f.read())

    assert workout.title == "Workout with variable"

    assert workout.content[0].volume.type == "fixed"
    assert workout.content[0].volume.variable == "interval_volume_variable"
    assert workout.content[0].intensity.type == "range"
    assert workout.content[0].intensity.variable == "interval_intensity_variable"

    assert workout.content[1].volume.type == "fixed"
    assert workout.content[1].volume.variable == "interval_volume_variable"
    assert workout.content[1].intensity.type == "ramp"
    assert workout.content[1].intensity.variable == "RAMP_VARIABLE"


def test_variable_fraction():
    with open("tests/test-data/variable-fraction.json", "r") as f:
        workout = Workout.model_validate_json(f.read())

    assert workout.title == "Workout with variable fraction"

    assert workout.content[0].intensity.type == "fixed"
    assert workout.content[0].intensity.variable == "threshold"
    assert workout.content[0].intensity.fraction == 0.5


def test_gpt_created():
    with open("tests/test-data/gpt-created.json", "r") as f:
        workout = Workout.model_validate_json(f.read())

    assert workout.title == "GPT Created Workout"


def test_single_variable():
    with open("tests/test-data/single-variable.json", "r") as f:
        workout = Workout.model_validate_json(f.read())
    
    variables = workout.get_intensity_variables()
    assert len(variables) == 1
    assert list(variables)[0] == "FTP"

    assert workout.has_only_one_intensity_variable()
    assert not workout.has_only_absolute_intensity()


def test_all_absolute_intensity():
    with open("tests/test-data/all-absolute-intensity.json", "r") as f:
        workout = Workout.model_validate_json(f.read())

    assert workout.has_only_absolute_intensity()
    assert not workout.has_only_one_intensity_variable()


def test_mixed_absolute_intensity():
    with open("tests/test-data/mixed-abolute-intensity.json", "r") as f:
        workout = Workout.model_validate_json(f.read())

    assert workout.has_only_absolute_intensity()
    assert not workout.has_only_one_intensity_variable()

def test_all_variables():
    with open("tests/test-data/all-variables.json", "r") as f:
        workout = Workout.model_validate_json(f.read())

    assert workout.get_intensity_variables() == {"FTP"}
    assert workout.get_volume_variables() == {"WARM_UP_DURATION", "INTERVAL_DURATION", "COOL_DOWN_DURATION"}
    assert workout.get_repeat_variables() == {"REPEAT_COUNT"}