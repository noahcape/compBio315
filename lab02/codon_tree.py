import sys

class Codon_Tree_Node:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []

    def set_child(self, child):
        for node in self.children:
            if (node.get_name() is child.get_name()):
                return False

        self.children.append(child)

    def get_name(self):
        return self.name

    def get_parent(self):
        return self.parent

    def is_leaf(self):
        return len(self.children) == 0

    def get_child(self, base):
        if ((base == None) & (len(self.children) == 1)):
            return self.children[-1]

        for node in self.children:
            if (node.get_name() == base):
                return node

        return None


class Codon_Tree:
    def __init__(self, file):
        self.root = Codon_Tree_Node("NONE", None)

        f = open(file, "r")

        for line in f:
            parent = self.root
            # dont read the new line character
            for elem in line[:-1]:
                node = self.add_node(parent, elem)

                parent = node

        f.close()
        

    def get_root(self):
        return self.root

    def find_aa(self, codon):
        cur_node = self.root
        index = 0

        while (index < len(codon)):
            cur_node = cur_node.get_child(codon[index])

            if (cur_node == None):
                return None

            index += 1

        return cur_node.get_child(None).get_name()

    def add_node(self, parent, name):
        node = parent.get_child(name)

        if (node == None):
            node = Codon_Tree_Node(name, parent)

        parent.set_child(node)

        return node


if __name__ == "__main__":
    tree = Codon_Tree(sys.argv[-1])

    aa = tree.find_aa("TCC")