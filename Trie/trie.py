import collections
collections.defaultdict(Node)

class Node():
  def __init__(self, key=None):
    self.key = key
    self.children = { }
    self.complete_string = False

class Trie():
  def __init__(self, key_list):
    if len(key_list) < 1:
      return
    self.root_node = Node(key_list[0]);
    for key in key_list[1:]:
      #node = Node(key)
      self.insert(key)
      
  def find(self, key):
    node = self.root_node
    for char in key:
      if node.children[char]:
        node = node.childeren[char]
      else:
        return False;
    return True;
  
  def insert(self, key):
    node = self.root_node
    for char in key:
      if node.children[char]:
        node = node.childeren[char]
      else:
        new_node = Node(char)
        node.childeren[char] = new_node
        node = new_node
    node.complete_string = True
  
  def remove(self, key):
    node = self.root_node
    suffixes = []
    
    for idx, char in enumerate(key):
      if node.children[char]:
        noded = node.children[char]
        #suffixes.unshift(node);
        suffixes.appendleft(node) #dequeue로 만들어야할듯?
        if (idx == len(key)) & len(node.children):
          print('error')
          return False
    
    for idx, char in enumerate(key):
      parent = suffixes[idx]
      child = key[len(suffixes) - idx]
      del parent.children[child]
      if parent.complete_string | len(parent.childrend):
        print('removed')
        return True
    
    del root_node.children[key[0]]  
    print ('root is removed')
    return True
  
  
if __name__ == '__main__':
  key_list = ['string', 'stringent', 'stringify', 'strings', 'strong', 'strung']
  Trie(key_list)
