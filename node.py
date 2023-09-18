class Node:
    def __init__(self, word: str) -> None:
        self.word = word
        self.children = {}
    
    def __str__(self):
        return f"<Node: {self.word}>"
    
    def __repr__(self):
        return str(self)
    
    def add_child(self, node: 'Node'):
        if node.word in self.children:
            return
        self.children[node.word] = node
    
    def add_word(self, word: str):
        if word not in self.children:
            new_node = Node(word)
            self.children[word] = new_node
        return self.children[word]
    
