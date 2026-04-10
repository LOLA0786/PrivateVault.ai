from coordination.mesh.merkle import MerkleTree

class MeshMerkleAnchor:

    def __init__(self):
        self.tree = MerkleTree()

    def anchor_message(self, message):
        return self.tree.add_leaf(message["hash"])

    def get_root(self):
        return self.tree.get_root()
