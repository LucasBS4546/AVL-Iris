from avltree import AvlTree


class AvlTreeIris(AvlTree):
    
    def insert(self, key, value):
        self.__setitem__(key, value)

    def find_closest(self, composite_index):
        pass

    def height(self):
        root_key = self._AvlTree__root_key
        if root_key is None:
            return -1

        nodes = self._AvlTree__nodes
        root_node = nodes.get(root_key)
        if root_node is None:
            return -1

        return root_node.height + 1

                

    def size(self):
        return self.__len__()