from typing import List, Tuple, Dict
import heapq

Coord = Tuple[int,int]

def neighbors(r,c,rows,cols):
    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r+dr, c+dc
        if 0<=nr<rows and 0<=nc<cols:
            yield nr,nc

def reconstruct(came, start, goal):
    if goal not in came: return []
    cur=goal; path=[cur]
    while cur!=start:
        cur=came[cur]; path.append(cur)
    path.reverse(); return path

def dijkstra(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    dist={start:0}; pq=[(0,start)]; came={}; visited=[]
    while pq:
        d,u = heapq.heappop(pq)
        if u in visited: continue
        visited.append(u)
        if u==goal: break
        ur,uc = u
        for v in neighbors(ur,uc,rows,cols):
            vr,vc=v
            if grid[vr][vc]==1: continue
            nd = d+1
            if nd < dist.get(v, float('inf')):
                dist[v]=nd; came[v]=u; heapq.heappush(pq, (nd, v))
    return {'visited': visited, 'path': reconstruct(came, start, goal)}

def manhattan(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])

def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    g={start:0}; f={start:manhattan(start,goal)}; pq=[(f[start],start)]; came={}; visited=[]
    while pq:
        _, u = heapq.heappop(pq)
        if u in visited: continue
        visited.append(u)
        if u==goal: break
        ur,uc = u
        for v in neighbors(ur,uc,rows,cols):
            vr,vc=v
            if grid[vr][vc]==1: continue
            tentative = g[u]+1
            if tentative < g.get(v, float('inf')):
                came[v]=u; g[v]=tentative; f[v]=tentative+manhattan(v,goal)
                heapq.heappush(pq, (f[v], v))
    return {'visited': visited, 'path': reconstruct(came, start, goal)}

def run_pathfinding(grid, start, goal, algorithm):
    if algorithm=='astar': return astar(grid, start, goal)
    return dijkstra(grid, start, goal)
