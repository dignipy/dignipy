class Node():
  def __init__(self, key=None):
    self.key = key
    self.children = self
    self.completeString = false;

class Trie():
  def __init__(self, key_list):
    if len(key_list) < 1:
      return false;
    self.rootNode = Node(key_list[0]);
    for key in key_list[1:]:
      node = Node(key)
      self.insert(node)
      
  def insert(key):
    node = self.rootNode
    for char in key:
      if node.children[char]:
        node = node.childeren[char]
      else:
        return false;
    return true;
  
  def find(key):
    pass
  
  def remove(key):
    pass
  
