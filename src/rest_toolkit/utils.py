_marker = []


def merge(base, overlay):
    """Recursively merge two dictionaries.

    This function merges two dictionaries. It is intended to be used to
    (re)create the full new state of a resource based on its current
    state and any changes passed in via a PATCH request. The merge rules
    are:

    * if a key `k` is present in `base` but missing in `overlay` it is
      untouched.
    * if a key `k` is present in both `base` and `overlay`:

      - and `base[k]` and `overlay[k]` are both dictionaries merge is
        applied recursively,
      - otherwise to value in `overlay` is used.

    * if a key `k` is not present in `base`, but is present in `overlay`
      it the value from `overlay` will be used.

    .. code-block:: python

       >>> merge({'foo': 'bar'}, {'foo': 'buz'})
       {'foo': 'buz'}
       >>> merge(['foo': 'bar'}, {'buz': True})
       {'foo': 'bar', 'buz': True}

    :param dict base: Dictionary with default data.
    :param dict overlay: Dictioanry with data to overlay on top of `base`.
    :rtype: dict
    :return: A copy of `base` with data from `overlay` added.
    """
    new_base = base.copy()
    for (key, new_value) in overlay.items():
        old_value = new_base.get(key, _marker)
        if old_value is _marker:
            new_base[key] = new_value
        elif isinstance(old_value, dict):
            if isinstance(new_value, dict):
                new_base[key] = merge(old_value, new_value)
            else:
                new_base[key] = new_value
        else:
            new_base[key] = new_value
    return new_base


def add_missing(data, defaults):
    for (key, value) in defaults.items():
        if key not in data:
            data[key] = value
    return data


__all__ = ['merge']
