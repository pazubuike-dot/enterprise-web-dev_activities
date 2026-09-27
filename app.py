import base64
import io
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from visualizer import linear_search, bubble_sort, binary_search, nested_loops, nested_loops2, test_stack_operations, test_queue_operations

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///analysis.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class AnalysisRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(50), nullable=False)
    n_max = db.Column(db.Integer, nullable=False)
    step = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="success")

with app.app_context():
    db.create_all()

ALGORITHMS = {
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

@app.route('/api/save_analysis', methods=['POST'])
def save_analysis():
    req_data = request.get_json()
    
    if not req_data:
        return jsonify({"error": "Invalid JSON or missing body"}), 400
    
    algo_name = req_data.get('algorithm', 'unknown')
    n_max = req_data.get('n_max', 0)
    step = req_data.get('step', 0)
    
    new_record = AnalysisRecord(
        algorithm=algo_name,
        n_max=n_max,
        step=step,
        status="success"
    )
    
    db.session.add(new_record)
    db.session.commit()
    
    return jsonify({
        "status": "success",
        "message": "Analysis data successfully saved to the database via SQLAlchemy!",
        "record_id": new_record.id
    }), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)