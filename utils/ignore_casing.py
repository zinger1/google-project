def ignore_casing(prefix):
    prefix = " ".join(prefix.split())
    prefix = "".join(filter(lambda x: x.isalnum() or x.isspace(), prefix)).lower()
    return prefix
