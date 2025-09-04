from typing import List, Tuple, Dict, Any

SORT_META: Dict[str, Dict[str, Any]] = {
    'bubble': {'name':'Bubble Sort','tc':'O(n^2)','sc':'O(1)'},
    'insertion': {'name':'Insertion Sort','tc':'O(n^2)','sc':'O(1)'},
    'selection': {'name':'Selection Sort','tc':'O(n^2)','sc':'O(1)'},
    'merge': {'name':'Merge Sort','tc':'O(n log n)','sc':'O(n)'},
    'quick': {'name':'Quick Sort','tc':'O(n log n) avg, O(n^2) worst','sc':'O(log n) avg recursion'},
    'heap': {'name':'Heap Sort','tc':'O(n log n)','sc':'O(1)'},
    'shell': {'name':'Shell Sort','tc':'varies ~O(n^(3/2))','sc':'O(1)'},
    'counting': {'name':'Counting Sort','tc':'O(n + k)','sc':'O(k)'},
    'radix': {'name':'Radix LSD','tc':'O(d*(n+k))','sc':'O(n + k)'},
    'bucket': {'name':'Bucket Sort','tc':'O(n + k)','sc':'O(n + k)'},
    'cocktail': {'name':'Cocktail Shaker Sort','tc':'O(n^2)','sc':'O(1)'},
    'comb': {'name':'Comb Sort','tc':'O(n^2) worst','sc':'O(1)'}
}

def generate_sort_steps(arr: List[int], algorithm: str) -> Tuple[List[Dict], List[int], List[str]]:
    a = arr[:]  # working copy
    steps: List[Dict] = []

    def rec_compare(i, j):
        steps.append({'compare':[i,j]})

    def rec_swap(i, j):
        steps.append({'swap':[i,j]})
        a[i], a[j] = a[j], a[i]

    def rec_set(i, val):
        steps.append({'set':[i,val]})
        a[i] = val

    def mark(indices, label):
        steps.append({'mark':{'indices':indices,'label':label}})

    n = len(a)
    if algorithm == 'bubble':
        for i in range(n):
            for j in range(0, n - i - 1):
                rec_compare(j, j+1)
                if a[j] > a[j+1]:
                    rec_swap(j, j+1)
        return steps, a, ['Simple pairwise swap until sorted.']

    if algorithm == 'insertion':
        for i in range(1,n):
            key = a[i]
            j = i-1
            while j>=0 and a[j]>key:
                rec_compare(j, j+1)
                rec_set(j+1, a[j])
                j -= 1
            rec_set(j+1, key)
        return steps, a, ['Insert each element into the sorted left part.']

    if algorithm == 'selection':
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                rec_compare(min_idx, j)
                if a[j] < a[min_idx]:
                    min_idx = j
            if min_idx != i:
                rec_swap(i, min_idx)
        return steps, a, ['Select min for each position.']

    if algorithm == 'merge':
        def merge(l, m, r):
            left = a[l:m]
            right = a[m:r]
            i=j=0
            k=l
            while i < len(left) and j < len(right):
                rec_compare(l+i, m+j)
                if left[i] <= right[j]:
                    rec_set(k, left[i]); i+=1
                else:
                    rec_set(k, right[j]); j+=1
                k+=1
            while i < len(left):
                rec_set(k, left[i]); i+=1; k+=1
            while j < len(right):
                rec_set(k, right[j]); j+=1; k+=1

        def ms(l,r):
            if r-l<=1: return
            m=(l+r)//2
            ms(l,m); ms(m,r); merge(l,m,r)
        ms(0,n)
        return steps, a, ['Divide-and-conquer merge.']

    if algorithm == 'quick':
        def partition(l,r):
            pivot = a[r]
            mark([r],'pivot')
            i=l
            for j in range(l,r):
                rec_compare(j,r)
                if a[j] <= pivot:
                    rec_swap(i,j); i+=1
            rec_swap(i,r); return i
        def qs(l,r):
            if l<r:
                p=partition(l,r)
                qs(l,p-1); qs(p+1,r)
        qs(0,n-1)
        return steps, a, ['Pick pivot and partition recursively.']

    if algorithm == 'heap':
        def heapify(sz, i):
            largest=i
            l=2*i+1; r=2*i+2
            if l<sz:
                rec_compare(l, largest)
                if a[l] > a[largest]: largest=l
            if r<sz:
                rec_compare(r, largest)
                if a[r] > a[largest]: largest=r
            if largest != i:
                rec_swap(i, largest); heapify(sz, largest)
        for i in range(n//2 -1, -1, -1): heapify(n, i)
        for i in range(n-1, 0, -1): rec_swap(0, i); heapify(i, 0)
        return steps, a, ['Binary heap sort.']

    if algorithm == 'shell':
        gap = n//2
        while gap>0:
            for i in range(gap,n):
                temp=a[i]; j=i
                while j>=gap and a[j-gap]>temp:
                    rec_compare(j-gap, j)
                    rec_set(j, a[j-gap]); j-=gap
                rec_set(j, temp)
            gap//=2
        return steps, a, ['Gap-based insertion passes.']

    if algorithm == 'counting':
        if any(x<0 for x in a):
            return [], a, ['Counting sort requires non-negative ints.']
        k = max(a) if a else 0
        count = [0]*(k+1)
        for v in a: count[v]+=1
        idx=0
        for val,cnt in enumerate(count):
            for _ in range(cnt): rec_set(idx, val); idx+=1
        return steps, a, ['Count frequency and overwrite.']

    if algorithm == 'radix':
        if any(x<0 for x in a):
            return [], a, ['Radix LSD implemented for non-negative ints.']
        exp=1
        maxv = max(a) if a else 0
        while maxv//exp>0:
            buckets=[[] for _ in range(10)]
            for i,val in enumerate(a):
                digit=(val//exp)%10
                buckets[digit].append(val)
                steps.append({'mark':{'indices':[i],'label':f'digit_{digit}'}})
            i=0
            for b in buckets:
                for v in b:
                    rec_set(i, v); i+=1
            exp*=10
        return steps, a, ['Radix sort (LSD).']

    if algorithm == 'bucket':
        if n==0: return steps, a, ['Empty array']
        bcount = min(n, 10)
        buckets=[[] for _ in range(bcount)]
        maxv=max(a); minv=min(a)
        if maxv==minv:
            return steps, a, ['All values same']
        for i,v in enumerate(a):
            idx = int((v-minv)/(maxv-minv+1e-9) * (bcount-1))
            buckets[idx].append(v); steps.append({'mark':{'indices':[i],'label':f'bucket_{idx}'}})
        pos=0
        for bi in range(len(buckets)):
            buckets[bi].sort()
            for v in buckets[bi]: rec_set(pos, v); pos+=1
        return steps, a, ['Bucket sort with simple buckets.']

    if algorithm == 'cocktail':
        swapped = True; start = 0; end = n-1
        while swapped:
            swapped = False
            for i in range(start, end):
                rec_compare(i, i+1)
                if a[i] > a[i+1]: rec_swap(i, i+1); swapped=True
            if not swapped: break
            swapped=False; end -=1
            for i in range(end-1, start-1, -1):
                rec_compare(i, i+1)
                if a[i] > a[i+1]: rec_swap(i, i+1); swapped=True
            start +=1
        return steps, a, ['Bidirectional bubble (cocktail).']

    if algorithm == 'comb':
        gap=n; shrink=1.3; sorted_flag=False
        while not sorted_flag:
            gap = int(gap/shrink)
            if gap<=1: gap=1; sorted_flag=True
            i=0
            while i+gap<n:
                rec_compare(i, i+gap)
                if a[i] > a[i+gap]: rec_swap(i, i+gap); sorted_flag=False
                i+=1
        return steps, a, ['Comb sort using shrinking gap.']

    return generate_sort_steps(arr, 'bubble')
