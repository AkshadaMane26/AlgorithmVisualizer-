from flask import Flask, render_template, request, jsonify, send_from_directory
from algorithms.sorting import generate_sort_steps, SORT_META
from algorithms.searching import generate_search_steps, SEARCH_META
from algorithms.pathfinding import run_pathfinding
from algorithms.mst_tsp import prim_mst_steps, kruskal_mst_steps, held_karp_tsp
from algorithms.linkedlist import LinkedListVisualizer

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/sorting')
def sorting_page():
    return render_template('sorting.html')

@app.route('/searching')
def searching_page():
    return render_template('searching.html')

@app.route('/path')
def path_page():
    return render_template('path.html')

@app.route('/linkedlist')
def linkedlist_page():
    return render_template('linkedlist.html')

@app.route('/api/sort', methods=['POST'])
def api_sort():
    data = request.get_json(force=True)
    algo = data.get('algorithm', 'bubble')
    arr = data.get('array', [])
    steps, final, dryrun = generate_sort_steps(arr, algo)
    meta = SORT_META.get(algo, {'name':algo,'tc':'?','sc':'?'})
    return jsonify({'steps': steps, 'final': final, 'dryrun': dryrun, 'meta': meta})

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.get_json(force=True)
    algo = data.get('algorithm', 'linear')
    arr = data.get('array', [])
    target = data.get('target')
    steps, found_index = generate_search_steps(arr, algo, target)
    meta = SEARCH_META.get(algo, {'name':algo,'tc':'?','sc':'?'})
    return jsonify({'steps': steps, 'found': found_index, 'meta': meta})

@app.route('/api/graph', methods=['POST'])
def api_graph():
    data = request.get_json(force=True)
    kind = data.get('kind')
    if kind in ('dijkstra','astar'):
        grid = data.get('grid')
        start = tuple(data.get('start'))
        goal = tuple(data.get('goal'))
        result = run_pathfinding(grid, start, goal, kind)
        return jsonify(result)
    if kind == 'prim':
        nodes = data.get('nodes')
        edges = data.get('edges')
        return jsonify(prim_mst_steps(nodes, edges))
    if kind == 'kruskal':
        nodes = data.get('nodes')
        edges = data.get('edges')
        return jsonify(kruskal_mst_steps(nodes, edges))
    if kind == 'tsp':
        dist_matrix = data.get('dist_matrix')
        n = len(dist_matrix)
        if n > 11:
            return jsonify({'error': 'TSP: n too large for exact Held-Karp demo (n <= 11 recommended).'}), 400
        tour, cost = held_karp_tsp(dist_matrix)
        return jsonify({'tour': tour, 'cost': cost})
    return jsonify({'error': 'Unknown graph kind'}), 400

@app.route('/api/linkedlist', methods=['POST'])
def api_linkedlist():
    data = request.get_json(force=True)
    action = data.get('action')
    payload = data.get('payload', {})
    vis = LinkedListVisualizer()
    initial = payload.get('initial', [])
    vis.build_from_list(initial)

    if action == 'insert_head':
        val = payload.get('value')
        steps = vis.insert_head(val)
        return jsonify({'steps': steps})
    if action == 'insert_tail':
        val = payload.get('value')
        steps = vis.insert_tail(val)
        return jsonify({'steps': steps})
    if action == 'insert_at':
        idx, val = payload.get('index'), payload.get('value')
        steps = vis.insert_at(idx, val)
        return jsonify({'steps': steps})
    if action == 'delete_at':
        idx = payload.get('index')
        steps = vis.delete_at(idx)
        return jsonify({'steps': steps})
    if action == 'reverse':
        steps = vis.reverse()
        return jsonify({'steps': steps})
    if action == 'search':
        val = payload.get('value')
        steps, idx = vis.search(val)
        return jsonify({'steps': steps, 'found': idx})
    return jsonify({'error': 'Unknown linkedlist action'}), 400

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('/mnt/data', filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
