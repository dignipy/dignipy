import collections

class Node():
  def __init__(self):
    self.children = collections.defaultdict(Node)
    self.complete_string = False

class Trie():
  def __init__(self, key_list):
    if len(key_list) < 1:
      return
    self.root_node = Node()
    for key in key_list:
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

  def insert_idiotway(self, key):
    node = self.root_node
    for char in key:    
      if char in node.children:
        node = node.children[char]
      else:
        new_node = Node(char)
        node.children[char] = new_node
        node = new_node
    node.complete_string = True
  
  def insert(self, key):
    node = self.root_node
    for char in key:
      node = node.children[char]
    node.complete_string = True
  
  def remove(self, key):
    node = self.root_node
    suffixes = collections.deque()
    
    for idx, char in enumerate(key):
      if node.children[char]:
        node = node.children[char]
        suffixes.appendleft(node)
        if (idx == len(key)) & len(node.children):
          print('error')
          return False
    
    for idx, char in enumerate(key):
      parent = suffixes[idx+1]
      child = key[len(suffixes) -1 -idx]
      del parent.children[child]
      if parent.complete_string | len(parent.children) == 0:
        print('removed')
        return True
    
    del root_node.children[key[0]]  
    print ('root is removed')
    return True
  
  
  
if __name__ == '__main__':
  key_list = ['string', 'stringfy', 'strong', 'strung']
  trie = Trie(key_list)
  print('find strung(expect True): ', trie.find('strung'))
  print('find strung(expect removed): ', end='')
  trie.remove('strung')
  print('find strung(expect False): ', trie.find('strung'))
  print('find strung(expect True): ', trie.find('string'))
  print('find strung(expect True): ', trie.find('strong'))
  print('find strung(expect True): ', trie.find('stringfy'))
