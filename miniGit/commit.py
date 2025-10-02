from blob import store_object

class Commit:
    def __init__(self, tree_hash, message, parent=None):
        self.tree_hash = tree_hash
        self.message = message
        self.parent = parent

    def store(self):
        commit_data = f"tree {self.tree_hash}\n"
        if self.parent:
            commit_data += f"parent {self.parent}\n"
        commit_data += f"\n{self.message}\n"
        return store_object(commit_data.encode(), "commit")
