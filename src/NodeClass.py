class NodeClass:
    def __init__(self):
        self.x = -1
        self.y = -1
        self.z = -1
        self.id = -1

    def __eq__(self, other):
        if isinstance(other, node):
            return self.x == other.x and self.y == other.y and self.z == other.z
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y, self.z))
    
    def __key(self):
        return (self.x, self.y, self.z)
