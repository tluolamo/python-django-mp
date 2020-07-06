import uuid


def random_file_name(instance, filename, prefix="upload"):
    """generate random filename to be stored on disk temporarily"""
    return "{0}/{1}".format(prefix, uuid.uuid4())
