from rcdsa.datastruct import HashMap

class LinkedHashMap(HashMap):

  class DataBinEx(HashMap.DataBin):
    def __init__(self, data=None, head=None, tail=None, treeified=False):
      super().__init__(data, treeified)
      self.head = head
      self.tail = tail
      self.size = 0
      
  class EntryEx(HashMap.Entry):
    def __init__(self, key=None, value=None, hash=None, next=None, before=None):
      super().__init__(key, value, hash, next)
      self.before = before

  def __init__(self, capacity=16, load_factor=0.75):
    super().__init__(capacity, load_factor)
    self.head = None
    self.tail = None

  def _resize(self):
    if old_table is None:
      self._table = [self.DataBinEx() for i in range(self._capacity)]
      return
    old_capacity = self._capacity
    old_threshold = self._threshold
    old_table = self._table
    self._capacity = self._capacity << 1
    self._threshold = self._threshold << 1
    self._table = [self.DataBinEx() for i in range(self._capacity)]
    for i in range(old_capacity):
      bin = old_table[i]
      if bin.data is None:
        continue
      elif not bin.treeified:
        self._move_linked_list(old_table, i, old_capacity, self._table)
      else:
        self._move_tree(old_table, i, old_capacity, self._table)

  def traversal_entry(self, callback):
    for bin in self._table:
      if bin.data is None:
        continue
      elif not bin.treeified:
        curr_entry = bin.data
        while curr_entry is not None:
          callback(curr_entry)
          curr_entry = curr_entry.next
      else:
        def _processor(entry):
          callback(entry)
        bin.data.traversal_preorder(_processor)


  def put(self, key, value, overwrite=True):
    if self._table is None:
      self._resize()
    hash = self._hash(key)
    entry = self.EntryEx(key, value, hash)
    bin = self._table[(self._capacity-1) & entry.hash]
    entry_presented = None
    
    # insert
    if bin.data is None:
      # linked list insert
      bin.data = entry
      bin.treeified = False
    elif not bin.treeified: 
      # linked list insert
      curr_entry = bin.data
      count = 0
      while True:
        if curr_entry.hash == hash and (curr_entry.key is key or curr_entry.key == key):
          entry_presented = curr_entry
          break
        if curr_entry.next is None:
          curr_entry.next = entry
          if count >= self._treeify_threshold-1:
            self._treeify(bin)
          break
        curr_entry = curr_entry.next
        count += 1
    else:
      # red-black tree insert
      entry_presented = bin.data.insert(entry)
    
    # overwrite
    if entry_presented is not None:
      if overwrite:
        entry_presented.value = value
    else:
      self._size += 1
      if self._size > self._threshold:
        self._resize()

  def remove(self, key):
    if self._table is None:
      self._resize()
    hash = self._hash(key)
    bin = self._table[(self._capacity-1) & hash]
    if bin.data is None:
      return
    elif not bin.treeified:
      curr_entry = bin.data
      curr_entry_parent = None
      while curr_entry is not None:
        if curr_entry.hash == hash and (curr_entry.key is key or curr_entry.key == key):
          break
        curr_entry_parent = curr_entry
        curr_entry = curr_entry.next
      if curr_entry is None:
        return
      elif curr_entry_parent is None:
        bin.data = None
        return curr_entry.value
      else:
        curr_entry_parent.next = curr_entry.next
        return curr_entry.value
    else:
      deleted_entry = bin.data.delete(self.Entry(key=key, hash=hash))
      if bin.data.is_empty():
        del bin.data
        bin.treeified = False
      if deleted_entry is not None:
        self._size -= 1
        return deleted_entry.value
