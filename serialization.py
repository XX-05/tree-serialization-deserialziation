import io
from node import Node


CODEC = {
    "N_CHILDREN": 0xf0
}


def encode_node(node: Node):
    n_children = len(node.children)
    n_children_bytes = 0
    if n_children > 0:
        n_children_bytes = int(n_children / 0xff) + 1
    endw = CODEC["N_CHILDREN"] + n_children_bytes
    return node.word.encode('ascii') + endw.to_bytes(1, 'big') + int.to_bytes(n_children, n_children_bytes, 'big')

def serialize_node(fw: io.BytesIO, node: Node):
    stack = [node]
    
    while stack:
        curr = stack.pop()
        fw.write(encode_node(curr))
        for child in curr.children.values():
            stack.append(child)


def stack_deflation(stack: 'list[tuple[Node, int]]', new_node: Node, new_node_n_children: int):
    parent, parent_children = stack.pop()
    parent.add_child(new_node)
    parent_children -= 1

    if parent_children > 0:
        stack.append((parent, parent_children))

    if new_node_n_children > 0:
        stack.append((new_node, new_node_n_children))

    while stack:
        if stack[-1][1] == 0:
            stack.pop()
        else:
            break



def deserialize(fr: io.BytesIO):
    root_node = None
    stack = []
    buff = b''

    b = f.read(1)

    while b:
        if int.from_bytes(b, 'big') >= CODEC["N_CHILDREN"]:
            word = buff.decode('ascii')
            buff = b''
            n_children_bytes = int.from_bytes(b, 'big') - CODEC["N_CHILDREN"]
            n_children = 0
            for _ in range(n_children_bytes):
                n_children = n_children << 8
                n_children = n_children | int.from_bytes(f.read(1), 'big')
            new_node = Node(word)

            print(word, n_children)

            if root_node is None:
                root_node = new_node
                stack.append((root_node, n_children))
                b = f.read(1)
                continue
                
            stack_deflation(stack, new_node, n_children)
        else:
            buff += b
        b = f.read(1)
    
    return root_node

if __name__ == "__main__":
    node = Node("root")
    node.add_word("hi")
    hey = node.add_word("hey")
    hey.add_word("buddy")

    with open("serial.bin", "wb") as f:
        serialize_node(f, node)

    with open("serial.bin", "rb") as f:
        print(f.read())
        f.seek(0)
        print(deserialize(f).children['hey'].children)
