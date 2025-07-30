import re


def natural_key(s: str):
    """Convert a string that has a trailing integer to a tuple of (string, int) for
    natural sorting, i.e. first lexicographically by the string part and then by
    the integer part.

    Parameters
    ----------
    s : str
        The string to be converted.

    Returns
    -------
    tuple
        A tuple containing the string part and the integer part.
    """
    # Match the trailing integer in the string
    match = re.search(r"(\d+)$", s)
    # If a match is found, split the string and convert the integer part to int
    return (
        s[: match.start()] if match else s,
        int(match.group()) if match else float("-inf"),
    )  # Use -inf (float) as fallback
