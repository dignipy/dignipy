import collections

class Node():
  def __init__(self, key=None):
    self.key = key
    self.children = collections.defaultdict(Node)
    self.complete_string = False

class Trie():
  def __init__(self, key_list):
    if len(key_list) < 1:
      return
    self.root_node = Node()
    #self.root_node[0] = key_list[0]
    for key in key_list:
      #node = Node(key)
      self.insert(key)
      
  def find(self, key):
    node = self.root_node
    for char in key:
      if char in node.children:
        node = node.children[char]
      else:
        return False;
    if node.complete_string:
      return True;
    else:
      return False;

  def find_prefix(self, key):
    node = self.root_node
    for char in key:
      if char in node.children:
        node = node.children[char]
      else:
        return False;
    return True;
  
  def insert(self, key):
    node = self.root_node
    for char in key:
      if char in node.children:
        node = node.children[char]
      else:
        new_node = Node(char)
        node.children[char] = new_node
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
  key_list = ['string', 'stringfy', 'strong', 'strung']
  trie = Trie(key_list)
  trie.find('string')
