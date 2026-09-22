import base64
import io
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request
from visualizer import linear_search, bubble_sort, binary_search, nested_loops, nested_loops2, test_stack_operations, test_queue_operations
 

app = Flask(__name__)

ALGORITHMS ={
    'linear_search': linear_search,
    'bubble_sort': bubble_sort,
    'binary_search': binary_search,
    'nested_loops': nested_loops,
    'nested_loops2': nested_loops2,
    'stack_ops': test_stack_operations,
    'queue_ops': test_queue_operations
}

@app.route('/analyze', methods=['GET'])
def analyze():
    algo_name = request.args.get('algo', 'linear_search')
    step = int(request.args.get('step', 10))
    n_max = int(request.args.get('n_max', 1000))
    n_min = 0

    if algo_name not in ALGORITHMS:
        return jsonify({'error': 'Algorithm not supported'}), 400

    algorithm = ALGORITHMS[algo_name]

    times = []
    input_sizes = list(range(n_min, n_max + 1, step))

    for n in input_sizes:
        start_time = time.time()
        algorithm(n)
        end_time = time.time()
        times.append(end_time - start_time)

    fig, ax = plt.subplots()
    ax.plot(input_sizes, times, '-o')
    ax.set_xlabel('Input Size')
    ax.set_ylabel('Running Time (seconds)')
    ax.set_title(f'Time Complexity: {algo_name}')

    plot_path = f'complexity_plot_{algo_name}.png'
    plt.savefig(plot_path)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)

    return jsonify({
        'algorithm': algo_name,
        'n_max': n_max,
        'step': step,
        'image_base64': image_base64
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)