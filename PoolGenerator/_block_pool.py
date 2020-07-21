# Mixed Pool
# Random Pool

class BlockPool:
    """Base class of block pools
    Generate a block pool by Args when constructed.
    Attributes:
        blocks: List of blocks in the pool
    """
    
    def __init__(self,init_block=None):
        self.blocks=[]
        if init_block!=None:
            self.blocks.append(init_block)
        else:
            self.blocks=[]
        return
    def __iter__(self):
        return iter(self.blocks)
    def __str__(self):
        info="Pool size:"+str(len(self.blocks))+"\n"
        for block in self.blocks:
            info+=str(block)+"\n"
        return info
    def __iadd__(self,block):
        self.blocks.append(block)