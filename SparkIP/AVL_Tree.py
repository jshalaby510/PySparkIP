# Based off https://www.geeksforgeeks.org/avl-tree-set-1-insertion/
class TreeNode(object):
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


# AVL Tree to store IP networks
class AVL_Tree(object):
    def __init__(self):
        self.length = 0

    # Helper function for ordering IP networks in the AVL tree
    @staticmethod
    def compareNetworks(net1, net2):
        if net1 is None:
            return -1
        if net2 is None:
            return 1

        netAddr1 = int(net1.network_address)
        netAddr2 = int(net2.network_address)
        if netAddr1 > netAddr2:
            return 1
        elif netAddr1 < netAddr2:
            return -1
        else:
            broadAddr1 = int(net1.broadcast_address)
            broadAddr2 = int(net2.broadcast_address)
            if broadAddr1 > broadAddr2:
                return 1
            elif broadAddr1 < broadAddr2:
                return -1
            else:
                if net1.version > net2.version:
                    return 1
                elif net1.version < net2.version:
                    return -1
                else:
                    return 0

    def insert(self, root, key):
        if not root:
            self.length += 1
            return TreeNode(key)
        elif self.compareNetworks(key, root.val) == -1:
            root.left = self.insert(root.left, key)
        elif self.compareNetworks(key, root.val) == 1:
            root.right = self.insert(root.right, key)
        else:
            return root

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and self.compareNetworks(key, root.left.val) == -1:
            return self.rightRotate(root)

        if balance < -1 and self.compareNetworks(key, root.right.val) == 1:
            return self.leftRotate(root)

        if balance > 1 and self.compareNetworks(key, root.left.val) == 1:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and self.compareNetworks(key, root.right.val) == -1:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root

        return self.getMinValueNode(root.left)

    def delete(self, root, key):
        if not root:
            return root

        elif self.compareNetworks(key, root.val) == -1:
            root.left = self.delete(root.left, key)

        elif self.compareNetworks(key, root.val) == 1:
            root.right = self.delete(root.right, key)

        else:
            if root.left is None:
                temp = root.right
                root = None
                self.length -= 1
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                self.length -= 1
                return temp

            temp = self.getMinValueNode(root.right)
            root.val = temp.val
            root.right = self.delete(root.right,
                                     temp.val)

        if root is None:
            return root

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balance = self.getBalance(root)

        if balance > 1 and self.getBalance(root.left) >= 0:
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.right) <= 0:
            return self.leftRotate(root)

        if balance > 1 and self.getBalance(root.left) < 0:
            root.left = self.leftRotate(root.left)
            return self.rightRotate(root)

        if balance < -1 and self.getBalance(root.right) > 0:
            root.right = self.rightRotate(root.right)
            return self.leftRotate(root)

        return root

    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))

        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    def preOrder(self, root):
        if not root:
            return
        print(f"{root.val}")
        self.preOrder(root.left)
        self.preOrder(root.right)

    def netIntersect(self, root, set2):
        if root is None:
            return
        temp = root
        intersectList = []
        while True:
            if set2.contains(temp.val):
                intersectList.append(temp.val)

            if temp.left is not None:
                temp = temp.left
            elif temp.right is not None:
                temp = temp.right
            else:
                return intersectList

    def returnAll(self, root):
        if root is None:
            return
        temp = root
        return_list = []
        while True:
            return_list.append(temp.val)
            if temp.left is not None:
                temp = temp.left
            elif temp.right is not None:
                temp = temp.right
            else:
                return return_list

    # To check if an IP network is in the tree
    @staticmethod
    def avl_search(root, key):
        if root is None or key is None:
            return False
        elif AVL_Tree.compareNetworks(key, root.val) == -1:
            return AVL_Tree.avl_search(root.left, key)
        elif AVL_Tree.compareNetworks(key, root.val) == 1:
            return AVL_Tree.avl_search(root.right, key)
        else:
            return True

    # To check if an IP address is in the tree
    @staticmethod
    def avl_search_ipAddr(root, key):
        if root is None or key is None:
            return False
        elif key in root.val:
            return True
        elif int(key) < int(root.val.network_address):
            return AVL_Tree.avl_search_ipAddr(root.left, key)
        elif int(key) > int(root.val.network_address):
            return AVL_Tree.avl_search_ipAddr(root.right, key)
