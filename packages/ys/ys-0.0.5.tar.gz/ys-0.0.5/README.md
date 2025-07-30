# ys
Special dicts

To install:	```pip install ys```

## Overview

The `ys` package provides specialized dictionary classes that extend the functionality of Python's standard `dict` and `collections.defaultdict`. These classes include:

- `keydefaultdict`: A defaultdict variant where the default value for a missing key is generated dynamically based on the key itself.
- `DictDefaultDict`: A dictionary that provides default values for missing keys based on a predefined dictionary of key-value pairs.
- `KeyPathDict`: An advanced dictionary allowing access and modification of nested dictionary values using a key path (a dot-separated string or a list of keys).

## Features

### `keydefaultdict`

This class behaves like `collections.defaultdict` but allows the default factory function to receive the missing key as an argument. This is useful when the default value for each key needs to be determined dynamically.

### `DictDefaultDict`

This dictionary class is initialized with another dictionary that specifies default values for certain keys. When accessing a key that does not exist in the `DictDefaultDict`, it will return the default value from the provided default dictionary if available.

### `KeyPathDict`

This dictionary class supports accessing and setting values through a key path. A key path can be a dot-separated string or a list of nested keys, allowing for deep access into nested dictionaries. This feature is particularly useful for dealing with complex, nested data structures.

## Usage Examples

### Using `keydefaultdict`

```python
from ys import keydefaultdict

def generate_default(key):
    return len(key)

kd = keydefaultdict(generate_default)
print(kd['hello'])  # Outputs 5, as the default factory uses the length of the key
```

### Using `DictDefaultDict`

```python
from ys import DictDefaultDict

defaults = {'missing': 'default value', 'another': 42}
dd = DictDefaultDict(defaults)
print(dd['missing'])  # Outputs 'default value'
print(dd['not_there'])  # Outputs KeyError as 'not_there' is not a predefined default
```

### Using `KeyPathDict`

```python
from ys import KeyPathDict

data = {
    'user': {
        'name': 'John Doe',
        'address': {
            'street': '123 Elm St',
            'city': 'Somewhere'
        }
    }
}
kpd = KeyPathDict(data)
print(kpd['user.address.street'])  # Outputs '123 Elm St'
kpd['user.address.zip_code'] = '12345'  # Adds a new nested key
print(kpd['user.address'])  # Outputs {'street': '123 Elm St', 'city': 'Somewhere', 'zip_code': '12345'}
```

These specialized dictionaries provide enhanced flexibility and functionality for handling complex data structures and dynamic default values in Python applications.