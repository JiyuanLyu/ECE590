import time
class TreeNode:
    def __init__(self, val, freq, left, right):
        self.val=val
        self.freq=freq
        self.left=left
        self.right=right
        self.cost = None
        pass
    def __str__(self):
        if self.left is None and self.right is None:
            return str(self.val)
        left = str(self.left) if self.left is not None else '()'
        right = str(self.right) if self.right is not None else '()'
        return '({} {} {})'.format(self.val,left,right)
        
    def computeCost(self):
        if self.cost is not None:
            return self.cost
        def helper(n,depth):
            if n is None:
                return 0
            return depth * n.freq + helper(n.left, depth+1) + helper(n.right, depth +1)
        self.cost = helper(self, 1)
        return self.cost
    pass
pass

# Your code here.
