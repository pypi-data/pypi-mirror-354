# Structured Workout Format (SWF)

This document describes a JSON format for representing structured workouts. The format supports various types of intervals, repeats, sections, and instructions, making it suitable for describing both simple and complex workouts.

The goal of `SWF` is to be simple and easy to understand, while also being flexible and powerful enough to represent complex workouts.
`SWF` should be also able to serve as an intermediate format for converting to (and from) other formats.

The `SWF` format is accompanied by a Python implementation that serves as an official reference implementation, but note that `SWF` is in no way intended to be limited or tied to Python.

## Simple Example

Here's the most basic example of a workout with a single interval in the Structured Workout Format:

```json
{
  "title": "Simple Run",
  "description": "A 10-minute run at constant pace",
  "content": [
    {
      "type": "interval",
      "volume": {
        "type": "fixed",
        "quantity": "duration",
        "value": 600
      },
      "intensity": {
        "type": "fixed",
        "quantity": "speed",
        "value": 3.33
      }
    }
  ]
}
```

## Quantities and Units

The format supports the following quantities with their respective units:

### Volume Quantities
- `duration`: Time in seconds
- `distance`: Distance in meters

### Intensity Quantities
- `speed`: Speed in meters per second (m/s)
- `power`: Power in watts (W)

## Value Specifications

Value specifications are used to specify the volume and intensity of intervals or the number of repeats in a repeat.
Their specific uses are explained in below, the generic structure is the same across all uses and explained in this section.

```json
{
  "title": null,
  "description": null,
  "content": [
    {
      "type": "interval",
      "volume": <--- THIS IS WHERE THE VALUE SPECIFICATION FOR VOLUME GOES,
      "intensity": <--- THIS IS WHERE THE VALUE SPECIFICATION FOR INTENSITY GOES
    }
  ]
}
```

There are three ways to specify values for quantities: fixed, range, and ramp.

### 1. Fixed Value Specification

A single specific value:

```json
{
  "type": "fixed",
  "quantity": "speed",
  "value": 3.33
}
```

### 2. Range Value Specification

A range between min and max values. Both `min_value` and `max_value` are optional - you can specify just one to create an open-ended range:

```json
{
  "type": "range",
  "quantity": "power",
  "min_value": 200,
  "max_value": 250
}
```

It is possible to specify only a minimum or maximum value, which creates an open-ended range:
```json
{
  "type": "range",
  "quantity": "speed",
  "min_value": 2.5
}
```


### 3. Ramp Value Specification

A linear progression from start to end. Both `start_value` and `end_value` are required:

```json
{
  "type": "ramp",
  "quantity": "speed",
  "start_value": 2.5,
  "end_value": 3.5
}
```

Please note that ramp value specifications require both `start_value` and `end_value` to be specified, they cannot be open-ended.


## Variables

Variables allow you to reference variables directly in your workout, allowing the creation of workout templates or workouts that scale with the athlete's ability. Each variable can only be used for one type of quantity (e.g., if used for speed, it cannot be used for power).

```json
{
  "type": "fixed",
  "quantity": "speed",
  "variable": "Z1"
}
```

You can also specify a fraction of a variable, useful for example for specifying a percentage of FTP:

```json
{
  "type": "fixed",
  "quantity": "power",
  "variable": "FTP",
  "fraction": 0.75
}
```

When using variables, you can still specify a value that will be used as a default, but it will be ignored when the variable  is specified.
```json
{
  "type": "fixed",
  "quantity": "power",
  "variable": "FTP",
  "fraction": 0.75,
  "value": 250
}
```

Range values can also use variables:

```json
{
  "type": "range",
  "quantity": "power",
  "variable": "Z2",
}
```

Please note that in this case, the variable should specify both `min_value` and `max_value`.

Alternatively, you can specify the bounds of the range as a fraction of the variable:

```json
{
  "type": "range",
  "quantity": "power",
  "variable": "FTP",
  "min_fraction": 0.7,
  "max_fraction": 0.8
}
```

Ramp values can also use variables:
```json
{
  "type": "ramp",
  "quantity": "power",
  "variable": "Z4",
}
```

Please note again that in this case, the `Z4` variable should specify both `start_value` and `end_value`.

Again, alternatively, you can specify the start and end of the ramp as a fraction of the variable:

```json
{
  "type": "ramp",
  "quantity": "power",
  "variable": "FTP",
  "start_fraction": 0.6,
  "end_fraction": 0.9
}
```

## Intervals

An interval combines volume and intensity, both specified using value specifications:

```json
{
  "type": "interval",
  "volume": {
    "type": "fixed",
    "quantity": "duration",
    "value": 300
  },
  "intensity": {
    "type": "fixed",
    "quantity": "speed",
    "value": 3.33
  }
}
```

## Sections

Sections help organize workouts into logical parts. The names "warm up", "main set", and "cool down" have special meaning:

```json
{
  "type": "section",
  "name": "warm up",
  "content": [
    {
      "type": "interval",
      "volume": {
        "type": "fixed",
        "quantity": "duration",
        "value": 600
      },
      "intensity": {
        "type": "fixed",
        "quantity": "speed",
        "value": 2.5
      }
    }
  ]
}
```

Sections can be nested within other sections or repeats.

## Repeats

Repeats allow you to specify recurring patterns. They can be nested within sections or other repeats. The repeat count can be a fixed number, a range, or a variable:

```json
{
  "type": "repeat",
  "count": {
    "type": "fixed",
    "quantity": "number",
    "value": 4
  },
  "content": [
    {
      "type": "interval",
      "volume": {
        "type": "fixed",
        "quantity": "duration",
        "value": 60
      },
      "intensity": {
        "type": "fixed",
        "quantity": "speed",
        "value": 4.0
      }
    }
  ]
}
```

Example with a range for repeat count:
```json
{
  "type": "repeat",
  "count": {
    "type": "range",
    "quantity": "number",
    "min_value": 3,
    "max_value": 5
  },
  "content": [
    // ... intervals ...
  ]
}
```

Example with a variable for repeat count:
```json
{
  "type": "repeat",
  "count": {
    "type": "fixed",
    "quantity": "number",
    "variable": "INTERVAL_COUNT"
  },
  "content": [
    // ... intervals ...
  ]
}
```

## Instructions

Instructions provide text guidance within the workout:

```json
{
  "type": "instruction",
  "text": "Focus on maintaining good form"
}
```

## Complete Example

Here's a simple complete workout with sections and repeats:

```json
{
  "title": "Basic Interval Session",
  "description": "A simple workout with warm up, intervals, and cool down",
  "content": [
    {
      "type": "section",
      "name": "warm up",
      "content": [
        {
          "type": "interval",
          "volume": {
            "type": "fixed",
            "quantity": "duration",
            "value": 600
          },
          "intensity": {
            "type": "fixed",
            "quantity": "speed",
            "value": 2.5
          }
        }
      ]
    },
    {
      "type": "section",
      "name": "main set",
      "content": [
        {
          "type": "repeat",
          "count": {
            "type": "fixed",
            "quantity": "number",
            "value": 3
          },
          "content": [
            {
              "type": "interval",
              "volume": {
                "type": "fixed",
                "quantity": "duration",
                "value": 180
              },
              "intensity": {
                "type": "fixed",
                "quantity": "speed",
                "value": 3.5
              }
            },
            {
              "type": "interval",
              "volume": {
                "type": "fixed",
                "quantity": "duration",
                "value": 60
              },
              "intensity": {
                "type": "fixed",
                "quantity": "speed",
                "value": 0
              }
            },
            {
              "type": "instruction",
              "text": "It is allowed to walk between intervals"
            }
          ]
        }
      ]
    },
    {
      "type": "section",
      "name": "cool down",
      "content": [
        {
          "type": "interval",
          "volume": {
            "type": "fixed",
            "quantity": "duration",
            "value": 300
          },
          "intensity": {
            "type": "fixed",
            "quantity": "speed",
            "value": 2.0
          }
        }
      ]
    }
  ]
}
```