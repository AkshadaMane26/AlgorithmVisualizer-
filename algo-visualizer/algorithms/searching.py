from typing import List, Tuple, Dict, Any
import math

SEARCH_META = {
    'linear': {'name':'Linear Search','tc':'O(n)','sc':'O(1)'},
    'binary': {'name':'Binary Search','tc':'O(log n)','sc':'O(1)','requires':'sorted array'},
    'jump': {'name':'Jump Search','tc':'O(sqrt(n))','sc':'O(1)','requires':'sorted array'},
    'interpolation': {'name':'Interpolation Search','tc':'O(log log n) average','sc':'O(1)','requires':'uniformly distributed sorted array'}
}

def generate_search_steps(arr: List[int], algorithm: str, target: int) -> Tuple[List[Dict], int]:
    steps=[]
    n=len(arr)
    if algorithm=='linear':
        for i,v in enumerate(arr):
            steps.append({'compare':[i,target]})
            if v==target:
                steps.append({'found':i}); return steps, i
        return steps, -1

    if algorithm=='binary':
        l=0; r=n-1
        while l<=r:
            m=(l+r)//2
            steps.append({'compare':[m,target]})
            if arr[m]==target: steps.append({'found':m}); return steps,m
            if arr[m] < target: l=m+1
            else: r=m-1
        return steps, -1

    if algorithm=='jump':
        step = int(math.sqrt(n))
        prev=0
        while prev < n and arr[min(n-1, prev+step-1)] < target:
            steps.append({'compare':[min(n-1, prev+step-1), target]})
            prev += step
        for i in range(prev, min(prev+step, n)):
            steps.append({'compare':[i,target]})
            if arr[i]==target: steps.append({'found':i}); return steps,i
        return steps, -1

    if algorithm=='interpolation':
        lo=0; hi=n-1
        while lo<=hi and target>=arr[lo] and target<=arr[hi]:
            if arr[hi]==arr[lo]:
                if arr[lo]==target: steps.append({'found':lo}); return steps, lo
                break
            pos = lo + int((target - arr[lo])*(hi-lo)/(arr[hi]-arr[lo]))
            steps.append({'compare':[pos, target]})
            if arr[pos]==target: steps.append({'found':pos}); return steps,pos
            if arr[pos] < target: lo = pos+1
            else: hi = pos-1
        return steps, -1

    return [], -1
