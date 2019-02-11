class Node():
  def __init__(self, key=None):
    self.key = key
    self.children = self
    self.complete_string = false;

class Trie():
  def __init__(self, key_list):
    if len(key_list) < 1:
      return false;
    self.root_node = Node(key_list[0]);
    for key in key_list[1:]:
      node = Node(key)
      self.insert(node)
      
  def find(key):
    node = self.root_node
    for char in key:
      if node.children[char]:
        node = node.childeren[char]
      else:
        return false;
    return true;
  
  def insert(key):
    node = self.root_node
    for char in key:
      if node.children[char]:
        node = node.childeren[char]
      else:
        new_node = Node(char)
        node.childeren[char] = new_node
        node = new_node
    node.complete_string = true;
  
  def remove(key):
    pass
  
