import hashlib
import os

MINIGIT_DIR = ".minigit"
OBJECTS_DIR = os.path.join(MINIGIT_DIR, "objects")


def store_object(data, obj_type):
    """Store object (blob/tree/commit) and return its hash."""
    header = f"{obj_type} {len(data)}".encode()
    full_data = header + b"\x00" + data
    oid = hashlib.sha1(full_data).hexdigest()

    if not os.path.exists(OBJECTS_DIR):
        os.makedirs(OBJECTS_DIR)

    path = os.path.join(OBJECTS_DIR, oid)
    with open(path, "wb") as f:
        f.write(full_data)

    return oid


class Blob:
    def __init__(self, filename):
        self.filename = filename

    def store(self):
        with open(self.filename, "rb") as f:
            data = f.read()
        return store_object(data, "blob")
