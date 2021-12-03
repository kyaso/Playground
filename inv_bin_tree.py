class Node:
    def __init__(self, val, left = None, right = None):
        self.val = val
        self.left = left
        self.right = right

# For each node swap child nodes
def invBinTree(root: Node):
    # Swap children
    tmp = root.left
    root.left = root.right
    root.right = tmp

    # Call this function recursively on left and right children
    if root.left is not None:
        invBinTree(root.left)
    if root.right is not None:
        invBinTree(root.right)
    
    return root

def printNode(node: Node):
    print("Node:", node.val)
    if node.left is not None:
        print("Left child:", node.left.val)
    if node.right is not None:
        print("Right child:", node.right.val)

def printBinTree(root: Node):
    printNode(root)

    if root.left is not None:
        printBinTree(root.left)
    if root.right is not None:
        printBinTree(root.right)

def main():
    node4 = Node(4)
    node5 = Node(5)
    node6 = Node(6)
    node7 = Node(7)

    node2 = Node(2, node4, node5)
    node3 = Node(3, node6, node7)

    node1 = Node(1, node2, node3)

    print("Original tree:")
    printBinTree(node1)

    invRoot = invBinTree(node1)

    print("Tree after inversion:")
    printBinTree(invRoot)

    pass

if __name__ == '__main__':
    main()
