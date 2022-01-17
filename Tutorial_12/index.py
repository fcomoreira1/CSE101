class Node:
    def __init__(self, key, value, left, right):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __eq__(self, other):
        return other != None \
           and self.key == other.key \
           and self.value == other.value \
           and self.left == other.left \
           and self.right == other.right 

    def __repr__(self):
        return f'Node({repr(self.key)}, {repr(self.value)}, {repr(self.left)}, {repr(self.right)})'

    def __str__(self):
        lines, _ = self._str_aux()
        return '\n'.join(lines)

    def _str_aux(self):
        # Recursive helper for __str__.
        # Returns lines (to be joined) and the horizontal position where
        # a branch from an eventual parent should be attached.
        label = f'{self.key}: {self.value}'

        # Leaf case
        if self.right is None and self.left is None:
            return [label], len(label) // 2
    
        if self.left is None:
            llines, lpos, lwidth, ltop0, ltop1, lfill = [], 0, 0, '', '', ''
        else:  # Recurse left
            llines, lpos = self.left._str_aux()
            lwidth = len(llines[0])
            ltop0 = lpos*' ' + ' ' + (lwidth - lpos - 1)*'_'
            ltop1 = lpos*' ' + '/' + (lwidth - lpos - 1)*' '
            lfill = lwidth*' '
            
        if self.right is None:
            rlines, rpos, rwidth, rtop0, rtop1, rfill = [], 0, 0, '', '', ''
        else:  # Recurse right
            rlines, rpos = self.right._str_aux()
            rwidth = len(rlines[0])
            rtop0 = rpos*'_' + ' ' + (rwidth - rpos - 1)*' '
            rtop1 = rpos*' ' + '\\' + (rwidth - rpos - 1)*' '
            rfill = rwidth*' '

        cfill = len(label)*' '
        
        # Extend llines or rlines to same length, filling with spaces (or '')
        maxlen = max(len(llines), len(rlines))
        llines.extend(lfill for _ in range(maxlen - len(llines)))
        rlines.extend(rfill for _ in range(maxlen - len(rlines)))
          
        res = []
        res.append(ltop0 + label + rtop0)
        res.append(ltop1 + cfill + rtop1)
        res.extend(lline + cfill + rline for (lline, rline) in zip(llines, rlines))
        
        return res, lwidth + len(label) // 2

    def search(self, key):
        # print(self)
        if key == self.key:
            return self.value
        if key > self.key:
            if self.right == None:
                return None
            return self.right.search(key)
        if key < self.key:
            if self.left == None:
                return None
            return self.left.search(key)

    def print_in_order(self):
        if self.left != None:
            self.left.print_in_order()
        print(f"{self.key}: {self.value}")
        if self.right != None:
            self.right.print_in_order()

    def add(self, key, value):
        if key == self.key:
            if value not in self.value:
                self.value.append(value)

        if key < self.key:
            if self.left == None:
                self.left = Node(key, [value], None, None)
            else:
                self.left.add(key, value)

        if key > self.key:
            if self.right == None:
                self.right = Node(key, [value], None, None)
            else:
                self.right.add(key, value)

    def write_in_order(self, filename):
        """Write all key: value pairs in the index tree
        to the named file, one entry per line.
        """
        with open(filename, 'w') as file:
            self.write_in_order_rec(file)

    def write_in_order_rec(self, file):
        """Recursive helper method for write_in_order."""
        if self.left != None:
            self.left.write_in_order_rec(file)
        file.write(f"{self.key}: {self.value}\n")
        if self.right != None:
            self.right.write_in_order_rec(file)

    def height(self):
        if self.left == None and self.right == None:
            return 0
        if self.right == None:
            return self.left.height() + 1
        if self.left == None:
            return self.right.height() + 1
        return max(self.right.height(), self.left.height()) + 1
    
    def list_in_order(self):
        list = []
        if self.left != None:
           list += self.left.list_in_order() 
        list.append((self.key, self.value))
        if self.right != None:
           list += self.right.list_in_order() 
        return list

def example_bst():
    sev = Node(7, 'Seven', None, None)
    thi = Node(13, 'Thirteen', None, None)
    six = Node(6, 'Six', None, sev)
    the = Node(3, 'Three', None, None)
    fur = Node(4, 'Four', the, six)
    fot = Node(14, 'Fourteen', thi, None)
    ten = Node(10, 'Ten', None, fot)
    root = Node(8, 'Eight', fur, ten)
    return root

def split_in_words_and_lowercase(line):
    """Split a line of text into a list of lower-case words."""
    parts = line.strip('\n').replace('-', ' ').replace("'", " ").replace('"', ' ').split()
    parts = [p.strip('",._;?!:()[]').lower() for p in parts]
    return [p for p in parts if p != '']

def construct_bst_for_indexing(filename):
    root = None
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            parts = split_in_words_and_lowercase(line)
            for part in parts:
                if root == None:
                    root = Node(part, [1], None, None)
                else:
                    root.add(part, i+1)
    return root

def generate_index(textfile, indexfile):
    construct_bst_for_indexing(textfile).write_in_order(indexfile)
    
def balanced_bst(sorted_list):
    """Return balanced BST constructed from sorted list."""
    return balanced_bst_rec(sorted_list, 0, len(sorted_list))

def balanced_bst_rec(sorted_list, lower, upper):
    """Recursive helper function for balanced_bst."""
    if lower >= upper:
        return None
    root_ind = (upper + lower) // 2 
    return Node(sorted_list[root_ind][0], sorted_list[root_ind][1], balanced_bst_rec(sorted_list,lower, root_ind), balanced_bst_rec(sorted_list, root_ind + 1, upper))
