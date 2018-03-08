def merge_dicts(a, b):
    """
    Merge dicts a and b, with values in b overriding a

    Merges at the the second level. i.e. Merges dict top level values
    :return: New dict
    """
    c = a.copy()
    for k in b:
        if k not in c:
            c[k] = b[k]
        else:
            c[k].update(b[k])
    return c