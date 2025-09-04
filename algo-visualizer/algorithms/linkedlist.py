from typing import Any, List, Tuple, Dict

class Node:
    def __init__(self, val, nxt=None):
        self.val = val; self.next = nxt

class LinkedListVisualizer:
    def __init__(self):
        self.head = None

    def build_from_list(self, arr: List[Any]):
        self.head = None
        tail = None
        for v in arr:
            node = Node(v)
            if not self.head: self.head = node; tail=node
            else: tail.next = node; tail=node

    def snapshot(self):
        res=[]; cur=self.head
        while cur:
            res.append(cur.val); cur=cur.next
        return res

    def insert_head(self, val):
        steps=[]
        steps.append({'action':'create_node', 'val':val})
        newn = Node(val, self.head)
        self.head = newn
        steps.append({'action':'insert_head', 'state':self.snapshot()})
        return steps

    def insert_tail(self, val):
        steps=[{'action':'create_node','val':val}]
        if not self.head:
            self.head=Node(val); steps.append({'action':'insert_head','state':self.snapshot()}); return steps
        cur=self.head
        while cur.next: cur=cur.next
        cur.next=Node(val)
        steps.append({'action':'insert_tail', 'state':self.snapshot()})
        return steps

    def insert_at(self, idx, val):
        steps=[{'action':'create_node','val':val}]
        if idx<=0:
            return steps + self.insert_head(val)
        cur=self.head; i=0
        while cur and i<idx-1:
            cur=cur.next; i+=1
        if not cur:
            return steps + [{'action':'error','msg':'Index out of range','state':self.snapshot()}]
        node = Node(val, cur.next); cur.next = node
        steps.append({'action':'insert_at','index':idx,'state':self.snapshot()})
        return steps

    def delete_at(self, idx):
        steps=[]
        if not self.head: return [{'action':'error','msg':'Empty list'}]
        if idx==0:
            steps.append({'action':'delete_head','val':self.head.val})
            self.head = self.head.next
            steps.append({'state':self.snapshot()}); return steps
        cur=self.head; i=0
        while cur.next and i<idx-1:
            cur=cur.next; i+=1
        if not cur.next: return [{'action':'error','msg':'Index out of range'}]
        steps.append({'action':'delete_at','index':idx,'val':cur.next.val})
        cur.next = cur.next.next
        steps.append({'state':self.snapshot()}); return steps

    def reverse(self):
        steps=[]
        prev=None; cur=self.head
        while cur:
            steps.append({'action':'reverse_step','current':cur.val})
            nxt=cur.next; cur.next = prev; prev=cur; cur=nxt
        self.head = prev
        steps.append({'action':'reversed','state':self.snapshot()})
        return steps

    def search(self, val):
        steps=[]; idx=0; cur=self.head
        while cur:
            steps.append({'action':'compare','index':idx,'val':cur.val})
            if cur.val==val: steps.append({'action':'found','index':idx}); return steps, idx
            cur=cur.next; idx+=1
        return steps, -1
