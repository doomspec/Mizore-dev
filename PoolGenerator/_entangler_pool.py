# Mixed Pool
# Random Pool

class EntanglerPool:
    """Base class of entangler pools
    Generate a entangler pool by Args when constructed.
    Attributes:
        entanglers: List of entanglers in the pool
    """
    entanglers=[]
    def __init__(self):
        return
    def __iter__(self):
        return iter(self.entanglers)
    def __str__(self):
        info="Pool size:"+str(len(self.entanglers))+"\n"
        for entangler in self.entanglers:
            info+=str(entangler)+"\n"
        return info
        