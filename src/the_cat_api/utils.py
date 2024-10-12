def remove_nones(dict_: dict) -> dict:
    """
    Returns the dictionary but without keys whose value is `None`.
    """
    result = {}
    for key, value in dict_.items():
        if value is not None:
            result[key] = value
    return result
