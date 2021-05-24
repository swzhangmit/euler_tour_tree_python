class Euler_Tour_Tree:
    class Represented_Node:
        def __init__(self, val, parent=None, children=[], first_ptr=None, last_ptr=None):
            self.val = val
            self.parent = parent
            self.children = children
            self.first_ptr = AVL_tree.AVL_node(0, represented=self) # First appearance of node in euler tour representation
            self.last_ptr = self.first_ptr                          # Last appearance of node in euler tour representation

        def get_val(self):
            return self.val

        def get_parent(self):
            return self.parent

        def get_children(self):
            return self.children

        def get_first_ptr(self):
            return self.first_ptr

        def get_last_ptr(self):
            return self.last_ptr

        def set_parent(self, p):
            self.parent = p

        def add_child(self, c):
            self.children.append(c)

        def remove(self, c):
            self.children.remove(c)
    
        def find_root(self):
            """
            Find root in represented graph
            """
            ptr = self.get_last_ptr()
            while ptr.parent:
                ptr = ptr.parent
            while ptr.left:
                ptr = ptr.left
            return ptr.represented
        
        def find_avl_root(self):
            """
            Find root of AVL Tree representation of Euler Tour 
            """
            ptr = self.get_last_ptr()
            while ptr.parent:
                ptr = ptr.parent
            return ptr

    def __init__(self, root):
        self.root = root
        self.avl = AVL_tree()

    def cut(self, v):
        """
        Cut v subtree from self
        """
        # remove link in represented
        v.parent.remove(v)
        v.parent = None

        # cut AVL tree
        left_T, v_subtree = self.avl.cutting(v.first_ptr, v.last_ptr)        
        return v_subtree

    def link(self, u, v):
        """
        Link u subtree to self as a child of v
        """
        self.avl.linking(u, v)

class AVL_tree:
    #Inner node class
    class AVL_node:
        """
        Node class to be used in the tree.
        Each node has a balance factor attribute representing 
        the longest downward path rooted at the node.
        """
        def __init__(self, data=None, left=None, right=None, balance=0, parent=None, height=0, represented=None):
            self.data = data
            self.left = left
            self.right = right
            self.parent = parent
            self.height = height
            self.represented = represented

            #used to balance the tree: balance = height(left subtree) - height(right subtree)
            #tree at node is balanced if the value is in [-1, 0, 1], else it is unbalanced
            self.balance = balance 
            return

    def __init__(self):
        self._root = None
        self._depth = None
        self._max_chars = None
        return

    def __str__(self):
        """
        Traverses and prints the binary tree in an organized and pretty way.
        Uses a BFS (level-order) traversal.
        """
        self.synchronizeFields()
        if (self._depth == 0):
            return ""
        s = ""
        queue = []
        level = 0
        queue.append((1, self._root))
        while len(queue):
            nodelev, node = queue.pop(0)
            if (not node):
                if ((self._depth - nodelev + 1) <= 0):
                    continue
                if (nodelev != level):
                    s += "\n"
                    s += " "*int((self._max_chars)*(2**(self._depth - nodelev) - 1))
                    level = nodelev
                s += " "*(self._max_chars)*(2**(self._depth - nodelev + 1) - 1)
                s += " "*self._max_chars
                queue.append((nodelev + 1, None))
                queue.append((nodelev + 1, None))
                continue
            if (nodelev != level):
                s += "\n"
                s += " "*(self._max_chars)*(2**(self._depth - nodelev) - 1)
                level = nodelev
            for i in range(int(self._max_chars - len(str(node.represented.val)))):
                s += "|"
            s += str(node.represented.val) 
            s += " "*(self._max_chars)*(2**(self._depth - nodelev + 1) - 1)
            if node.left:
                queue.append((nodelev + 1, node.left))
            else:
                queue.append((nodelev + 1, None))
            if node.right:
                queue.append((nodelev + 1, node.right))
            else:
                queue.append((nodelev + 1, None))
        s += "\n"
        return s

    def synchronizeFields(self):
        """
        Calculates depth and max_chars of the tree
        """
        if (not self.getRoot()):
            self._depth = 0
            self._max_chars = 1
            return
        self._depth = 0
        self._max_chars = 1
        Q = []
        Q.append((self.getRoot(), 1, len(str(self.getRoot().data))))
        while len(Q):
            node, depth, chars = Q.pop(0)
            self._depth = max(self._depth, depth)
            self._max_chars = max(self._max_chars, chars)
            if node.left:
                Q.append((node.left, depth + 1, len(str(node.left.data))))
            if node.right:
                Q.append((node.right, depth + 1, len(str(node.right.data))))
        return

    def getRoot(self):
        return self._root

    def setRoot(self, node):
        self._root = node

    def contains(self, data):
        """
        External method used to search the tree for a data element.
        """
        return True if self.recursiveContains(data, self.getRoot()) else False

    def recursiveContains(self, data, node):
        """
        Internal method used to recursively search for data elements
        """
        if not node:
            return None
        elif node.data == data:
            return node
        elif data > node.data:
            return self.recursiveContains(data, node.right)
        elif data < node.data:
            return self.recursiveContains(data, node.right)

    def insertList(self, l):
        """
        Builds the tree by inserting elements from a list in order.
        """
        if (l == None):
            return
        try:
            for ele in l:
                self.insert(ele)
        except TypeError:
            return
        return

    def insert(self, data):
        """
        This is the external insert method for the data structure.
        Args:
            data: a data object to be inserted into the tree
        """
        if (data == None):
            return 
        if (not self.getRoot()):
            self.setRoot(AVL_tree.AVL_node(data=data))
            return
        else:
            self._done = 0
            self.recursiveInsert(self.getRoot(), data)
            delattr(self, "_done")
            return

    def recursiveInsert(self, node, data):
        """
        This is an internal method used to insert data elements 
        recursively into the tree.
        """

        #no duplicates in the tree
        if (data == node.data):
            return

        if data < node.data:
            if node.left:
                self.recursiveInsert(node.left, data)
            else:
                node.left = AVL_tree.AVL_node(data=data, parent=node)
                self.updateBalance(node.left)
        else:
            if node.right:
                self.recursiveInsert(node.right, data)
            else:
                node.right = AVL_tree.AVL_node(data=data, parent=node)
                self.updateBalance(node.right)
        return

    def updateBalance(self, node):
        """
        Balances the tree starting with a newly inserted node (node)
        """
        if (node.balance > 1 or node.balance < -1):
            self.rebalance(node)
            return
        if node.parent:
            if node.parent.left is node: #lchild
                if node.parent.balance >= 0:
                    node.parent.height += 1
                node.parent.balance += 1
            elif node.parent.right is node: #rchild
                if node.parent.balance <= 0:
                    node.parent.height += 1
                node.parent.balance -= 1

            #recurses to the parent
            if node.parent.balance != 0:
                self.updateBalance(node.parent)

    def rotateLeft(self, node):
        """
        Performs a left rotation.
        """
        print("rotating left around: " + str(node.represented.val))
        newRootNode = node.right
        node.right = newRootNode.left
        if (newRootNode.left):
            newRootNode.left.parent = node
        newRootNode.parent = node.parent
        if node is self.getRoot():
            self.setRoot(newRootNode)
        else:
            if node.parent.left is node:
                node.parent.left = newRootNode
                
            else:
                node.parent.right = newRootNode
            # change parent height 
            #node.parent.height -= 1
            parent_left_height = node.parent.left.height if node.parent.left else -1
            parent_right_height = node.parent.right.height if node.parent.right else -1
            node.parent.height = max(parent_left_height, parent_right_height) + 1

        newRootNode.left = node
        node.parent = newRootNode
        node.balance = node.balance + 1 - min(newRootNode.balance, 0)
        newRootNode.balance = newRootNode.balance + 1 + max(node.balance, 0)

        # Update height
        node_left_height = node.left.height if node.left else -1
        node_right_height = node.right.height if node.right else -1
        node.height = max(node_left_height, node_right_height) + 1

        newRoot_right_height = newRootNode.right.height if newRootNode.right else -1
        newRoot_left_height = newRootNode.left.height if newRootNode.left else -1
        newRootNode.height = max(newRoot_left_height, newRoot_right_height) + 1

        # Verify balances match height differences
        assert node_left_height - node_right_height == node.balance
        #print("node: ", node.data, ", newRoot: ", newRootNode.data)
        #print(newRoot_left_height, " - ", newRoot_right_height, " = ", newRootNode.balance)
        assert newRoot_left_height - newRoot_right_height == newRootNode.balance

    def rotateRight(self, node):
        """
        Performs a right rotation.
        """
        print("rotating right around: " + str(node.represented.val))
        newRootNode = node.left
        node.left = newRootNode.right
        if (newRootNode.right):
            newRootNode.right.parent = node
        newRootNode.parent = node.parent
        if node is self.getRoot():
            self.setRoot(newRootNode)
        else:
            if node.parent.right is node:
                node.parent.right = newRootNode
            else:
                node.parent.left = newRootNode
            # change parent height 
            parent_left_height = node.parent.left.height if node.parent.left else -1
            parent_right_height = node.parent.right.height if node.parent.right else -1
            node.parent.height = max(parent_left_height, parent_right_height) + 1

        newRootNode.right = node
        node.parent = newRootNode
        node.balance = node.balance - 1 - max(newRootNode.balance, 0)
        newRootNode.balance = newRootNode.balance - 1 + min(node.balance, 0)
  
        # Update height
        node_left_height = node.left.height if node.left else -1
        node_right_height = node.right.height if node.right else -1
        node.height = max(node_left_height, node_right_height) + 1

        newRoot_right_height = newRootNode.right.height if newRootNode.right else -1
        newRoot_left_height = newRootNode.left.height if newRootNode.left else -1
        newRootNode.height = max(newRoot_left_height, newRoot_right_height) + 1

        # Verify balances match height differences
        assert node_left_height - node_right_height == node.balance
        #print("node: ", node.data, ", newRoot: ", newRootNode.data)
        #print(newRoot_left_height, " - ", newRoot_right_height, " = ", newRootNode.balance)
        assert newRoot_left_height - newRoot_right_height == newRootNode.balance

    def rebalance(self, node):
        """
        Performs the tree rotations to rebalance the tree.
        """
        if node.balance < 0:
            if node.right.balance > 0:
                self.rotateRight(node.right)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balance > 0:
            if node.left.balance < 0:
                self.rotateLeft(node.left)
                self.rotateRight(node)
            else:
                self.rotateRight(node)
    
    def rebalance_node_to_root(self, node):
        while node:
            if abs(node.balance) > 1:
                self.rebalance(node)
            node = node.parent


    def update_height(self, node):
        """
        start at a given node and traverse upwards to update
        the height and balance from the node to the root
        """
        while node != None:
            node_left_height = node.left.height if node.left else -1
            node_right_height = node.right.height if node.right else -1
            node.height = 1 + max(node_left_height, node_right_height)
            node.balance = node_left_height - node_right_height
            node = node.parent


    def find_min(self):
        """
        find min of the tree by traversing left
        """
        node = self._root
        while node.left != None:
            node = node.left
        return node

    def find_max(self):
        """
        find max of the tree by traversing right
        """
        node = self._root
        while node.right != None:
            node = node.right
        return node

    def concatenate(self, other):
        """
        concatenate two AVL trees where the largest key in one tree
        is less than the smallest key in the other. concatenation is
        done by redirecting a pointers to roots, min, max, and nodes
        at particular heights. 
        More detail here: https://dhruvbird.blogspot.com/2014/01/merging-avl-trees.html
        """

        T1 = self 
        T2 = other 

        T1.synchronizeFields()
        T2.synchronizeFields()
        h1 = T1._depth
        h2 = T2._depth

        if h1 >= h2:
        # delete the smallest element x from T2, leaving T'2 of height h
            x = T2.find_min()

            if T2.getRoot() is x and T2.getRoot() is T2.find_max():
                # if the smallest element x is the only node in T2
                T1_max = T1.find_max()
                T1_max.right = T2.getRoot()
                T2.getRoot().parent = T1_max
                T2.getRoot().height = 0
                T1.update_height(T2.getRoot())
                T1.rebalance(T1.getRoot())
                return T1

            if x is not T2.getRoot():
                # if the smallest element x is the root of T2
                x_parent = x.parent
                if x is x.parent.right:
                    x.parent.right = None
                else:
                    x.parent.left = None
                x.parent = None
                T2.update_height(x_parent)
                T2.rebalance_node_to_root(x_parent)
                h = T2.getRoot().height
            else:
                if x.right:
                    T2.setRoot(x.right)
                    x.right.parent = None
                    x.right = None
                T2.update_height(T2.getRoot())
                T2.rebalance(T2.getRoot())
                h = T2.getRoot().height

            # find v, the rightmost path from the root of T1 whose height is either         
            T1.update_height(T1.find_max())
            v = T1.getRoot()
            while v.height != h+1 and v.height != h:
                v = v.right
            u = v.parent

            x.left = v
            x.right = T2.getRoot()
            v.parent = x
            T2.getRoot().parent = x

            if u:
                # if u exists, update the height starting from u
                u.right = x
                x.parent = u
                T1.update_height(x)
                T1.rebalance(u)
            else:
                T1.setRoot(x)
            return T1

        else: 
            x = T1.find_max()
            if T1.getRoot() is x and T1.getRoot() is T1.find_min(): 
                T2_min = T2.find_min()
                T2_min.left = T1.getRoot()
                T1.getRoot().parent = T2_min
                T1.getRoot().height = 0
                T2.update_height(T1.getRoot())
                T2.rebalance(T2.getRoot())
                return T2 

            if x is not T1.getRoot():
                x_parent = x.parent
                if x is x.parent.right:
                    x.parent.right = None
                else:
                    x.parent.left = None
                x.parent = None
                T1.update_height(x_parent)
                T1.rebalance_node_to_root(x_parent)
                h = T1.getRoot().height

            else:
                if x.left:
                    T1.setRoot(x.left)
                    x.left.parent = None
                    x.left = None
                T1.update_height(T1.getRoot())
                T1.rebalance(T1.getRoot())
                h = T1.getRoot().height

            T2.update_height(T2.find_min())
            v = T2.getRoot()
            while v.height != h+1 and v.height != h:
                v = v.right
            u = v.parent

            x.left = T1.getRoot()
            x.right = v
            v.parent = x
            T1.getRoot().parent = x 

            if u:
                u.left = x
                x.parent = u
                T2.update_height(x)
                T2.rebalance(u)
            else:
                T2.setRoot(x)
            return T2

    
    def split(self, v, sign):
        """
        Split self AVL Tree in two sections, lt and rt, with lt being elements less than v, and rt being elements greater than v.
        If sign is True:
            v goes with rt
        If sign is False:
            v goes with lt
        """
        # Outer/Left Pointer
        lt = None
        if sign:
            lt = v.left if v.left else None
        else:
            lt = v.right if v.right else None
        
        # Inner/Right Pointer
        rt = v
        
        ancestor = v.parent
        
        # boolean representing whether ancestor is greater or less than v
        increase = True
        if (ancestor and ancestor.right == v):
            increase = False

        # Traverse up v's parent pointers, redirecting pointers to "unzip" the BST bottom up
        while ancestor != None:
            if (not increase and sign) or (increase and not sign):
                if sign:
                    ancestor.right = lt
                else:
                    ancestor.left = lt

                if lt:
                    lt.parent = ancestor
                lt = ancestor
                # recomputing height and balance
                lt_left_height = lt.left.height if lt.left else -1
                lt_right_height = lt.right.height if lt.right else -1
                lt.height = 1 + max(lt_left_height, lt_right_height)
                lt.balance = lt_left_height - lt_right_height

            else:
                if sign:
                    ancestor.left = rt
                else:
                    ancestor.right = rt
                
                if rt:
                    rt.parent = ancestor
                rt = ancestor
                # recomputing height and balance
                rt_left_height = rt.left.height if rt.left else -1
                rt_right_height = rt.right.height if rt.right else -1
                rt.height = 1 + max(rt_left_height, rt_right_height)
                rt.balance = rt_left_height - rt_right_height

            prev = ancestor
            ancestor = prev.parent
            if ancestor:
                # recomputing height and balance
                ancestor_left_height = ancestor.left.height if ancestor.left else -1
                ancestor_right_height = ancestor.right.height if ancestor.right else -1
                ancestor.height = 1 + max(ancestor_left_height, ancestor_right_height)
                ancestor.balance = ancestor_left_height - ancestor_right_height
            if ancestor and ancestor.right == prev:
                increase = False
            else:
                increase = True

        # return (root of left tree, root of right tree)
        return (lt, rt)
        
    def cutting(self, first_v, last_v):
        """
        Cut out v subtree from euler tour representation
        """
        # split by first appearance of v in euler tour
        lt, rt = self.split(first_v, True)
        
        middle_T = AVL_tree()
        middle_T.setRoot(rt)

        # split by last appearance of v in euler tour
        lt2, rt2 = middle_T.split(last_v, False)

        left_T = AVL_tree()
        left_T.setRoot(lt)
        left_T.rebalance(left_T.getRoot())

        right_T = AVL_tree()
        right_T.setRoot(lt2)
        right_T.rebalance(right_T.getRoot())

        v_subtree = AVL_tree()
        v_subtree.setRoot(rt2)
        v_subtree.rebalance(v_subtree.getRoot())
       
        # concatenate and return subtree before first appearance of v and subtree after last appearance of v
        # return cut out v subtree
        return left_T.concatenate(right_T), v_subtree

    def linking(self, u, v):
        """
        Link u subtree as a child of v in euler tour representation
        """
        # Update represented tree
        # append v to w's children
        v.add_child(u)
        # set v's parent to w
        u.set_parent(v)

        # Update AVL Tree
        # split based on last appearance of v in AVL Tree
        v_ptr = v.get_last_ptr()
        lt, rt = self.split(v_ptr, True)
        ut = u.find_avl_root()

        left_T = AVL_tree()
        left_T.setRoot(lt)

        # Insert singleton v as rightmost element of left subtree
        if lt:
            ptr = left_T.getRoot()
            while (ptr.right != None):
                ptr = ptr.right

            ptr.right = AVL_tree.AVL_node(parent=ptr, represented=v)
            ptr.balance -= 1

            while (ptr.parent != None):
                ptr = ptr.parent
                ptr_left_height = ptr.left.height if ptr.left else -1
                ptr_right_height = ptr.right.height if ptr.right else -1
                ptr.height = 1 + max(ptr_left_height, ptr_right_height)
                ptr.balance = ptr_left_height - ptr_right_height

            left_T.rebalance(left_T.getRoot())

        right_T = AVL_tree()
        right_T.setRoot(rt)
        right_T.rebalance(right_T.getRoot())

        u_subtree = AVL_tree()
        u_subtree.setRoot(ut)
        u_subtree.rebalance(u_subtree.getRoot())

        if lt:
            # concatenate left subtree with u subtree
            self = left_T.concatenate(u_subtree)
        else:
            self = u_subtree
            ptr = self.getRoot()
            
            while (ptr.left != None):
                ptr = ptr.left
            
            ptr.left = AVL_tree.AVL_node(parent=ptr, represented=v)
            ptr.balance += 1

            while (ptr.parent != None):
                ptr = ptr.parent
                # recompute heights and balances
                ptr_left_height = ptr.left.height if ptr.left else -1
                ptr_right_height = ptr.right.height if ptr.right else -1
                ptr.height = 1 + max(ptr_left_height, ptr_right_height)
                ptr.balance = ptr_left_height - ptr_right_height
                
            self.rebalance(self.getRoot())

        # concatenate with right subtree
        self = self.concatenate(right_T)
        print("result: ", self)

        
root = Euler_Tour_Tree.Represented_Node(1)
euler = Euler_Tour_Tree(root)

assert(1 == euler.root.find_root().val)

print("Add 2 as a child of 1: ")
node0 = Euler_Tour_Tree.Represented_Node(2)
euler.link(node0, root)

print("Add 3 as a child of 1: ")
node1 = Euler_Tour_Tree.Represented_Node(3)
euler.link(node1, root)

print("Add 4 as a child of 3: ")
node2 = Euler_Tour_Tree.Represented_Node(4)
euler.link(node2, node1)

print("Add 5 as a child of 1: ")
node3 = Euler_Tour_Tree.Represented_Node(5)
euler.link(node3, root)
