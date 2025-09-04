from typing import List, Tuple, Dict, Any

def prim_mst_steps(nodes: List[int], edges: List[Tuple[int,int,int]]):
    adj = {u:[] for u in nodes}
    for u,v,w in edges:
        adj[u].append((v,w)); adj[v].append((u,w))
    import heapq
    start=nodes[0]
    visited=set([start])
    pq=[]
    for v,w in adj[start]: heapq.heappush(pq,(w,start,v))
    steps=[]; mst_edges=[]
    while pq and len(visited) < len(nodes):
        w,u,v = heapq.heappop(pq)
        if v in visited: continue
        steps.append({'select_edge':(u,v,w)})
        visited.add(v); mst_edges.append((u,v,w))
        for x,wx in adj[v]:
            if x not in visited: heapq.heappush(pq,(wx,v,x))
    total = sum(w for _,_,w in mst_edges)
    return {'steps': steps, 'mst': mst_edges, 'cost': total}

class DSU:
    def __init__(self,nodes):
        self.p = {x:x for x in nodes}
        self.r = {x:0 for x in nodes}
    def find(self,x):
        while self.p[x]!=x: x=self.p[x]
        return x
    def union(self,a,b):
        ra, rb = self.find(a), self.find(b)
        if ra==rb: return False
        if self.r[ra] < self.r[rb]: self.p[ra]=rb
        elif self.r[rb] < self.r[ra]: self.p[rb]=ra
        else: self.p[rb]=ra; self.r[ra]+=1
        return True

def kruskal_mst_steps(nodes, edges):
    edges_sorted = sorted(edges, key=lambda x: x[2])
    dsu = DSU(nodes)
    mst=[]; steps=[]
    for u,v,w in edges_sorted:
        steps.append({'consider_edge':(u,v,w)})
        if dsu.union(u,v):
            steps.append({'take_edge':(u,v,w)})
            mst.append((u,v,w))
    cost = sum(w for _,_,w in mst)
    return {'steps':steps, 'mst':mst, 'cost':cost}

def held_karp_tsp(dist_matrix):
    n = len(dist_matrix)
    dp = {}
    parent = {}
    for i in range(1, n):
        dp[(1<<i, i)] = dist_matrix[0][i]
    for mask in range(0, 1<<n):
        for j in range(1, n):
            if not (mask & (1<<j)): continue
            prev_mask = mask ^ (1<<j)
            if prev_mask == 0 and j!=0: continue
            candidates = []
            for k in range(1, n):
                if k==j or not (prev_mask & (1<<k)): continue
                prev = dp.get((prev_mask, k), float('inf')) + dist_matrix[k][j]
                candidates.append((prev, k))
            if candidates:
                best, pk = min(candidates)
                dp[(mask,j)] = best
                parent[(mask,j)] = pk
    full_mask = (1<<n)-1
    best_cost = float('inf'); last = -1
    for j in range(1,n):
        cost = dp.get((full_mask ^ 1, j), float('inf')) + dist_matrix[j][0]
        if cost < best_cost: best_cost = cost; last = j
    if best_cost==float('inf'):
        return [], float('inf')
    mask = full_mask ^ 1; tour=[0, last]
    while mask:
        prev = parent.get((mask, last))
        tour.append(prev); mask ^= (1<<last); last = prev
    tour.reverse()
    return tour, best_cost
