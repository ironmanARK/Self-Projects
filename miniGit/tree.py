from blob import store_object

class Tree:
    def __init__(self, entries):
        # entries = {filename: blob_hash}
        self.entries = entries

    def store(self):
        tree_data = ""
        for filename, blob_hash in self.entries.items():
            tree_data += f"{blob_hash} {filename}\n"
        return store_object(tree_data.encode(), "tree")
