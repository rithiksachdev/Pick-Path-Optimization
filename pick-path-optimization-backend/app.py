from flask import Flask, request
import pandas as pd
from flask_cors import CORS,  cross_origin

from waveSimulation import (
	simulation_wave,
	simulate_batch
)
from clusterSimulation import(
	loop_wave,
	simulation_cluster,
	create_dataframe,
	process_methods
)

from getRoute import simulation_cluster_for_route

from getRoute2 import simulate_batch_route

app = Flask(__name__)
CORS(app)

# Preparation of data
def load(filename, n):
    print(n)
    df_orderlines = pd.read_csv(IN + filename).head(n)
    return df_orderlines


# Alley Coordinates on y-axis
y_low, y_high = 5.5, 50
# Origin Location
origin_loc = [0, y_low]
# Distance Threshold (m)
IN = 'static/in/'
# Store Results by WaveID
list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = [], [], [], [], [], [], []
list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]	# Group in list
# Store Results by Simulation (Order_number)
list_ordnum , list_dstw = [], []


@app.route('/')
def index():
    return "Hello, World!"

@app.route('/simulate-n-wave-orders',methods = ['POST'])
@cross_origin(origin='*')
def simulateNWaveOrders():
    print(request.args)
    list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = [], [], [], [], [], [], []
    list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]	# Group in list
    # Store Results by Simulation (Order_number)
    list_ordnum , list_dstw = [], []

    lines_number = int(request.args.get('lines_number'))
    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))
    y_low = float(request.args.get('y_low'))
    y_high = float(request.args.get('y_high'))
    df_orderlines = load('df_lines.csv', lines_number)
    origin_loc = [0, y_low]
    df_waves, df_results = simulate_batch(n1, n2, y_low, y_high, origin_loc, lines_number, df_orderlines)
    return df_results.to_dict()

@app.route('/simulate-n-batch-orders',methods = ['POST'])
def simulateNBatchOrders():
    print(request.args)
    list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = [], [], [], [], [], [], []
    list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]	# Group in list
    # Store Results by Simulation (Order_number)
    list_ordnum , list_dstw = [], []

    lines_number = int(request.args.get('lines_number'))
    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))
    y_low = float(request.args.get('y_low'))
    y_high = float(request.args.get('y_high'))
    distance_threshold = float(request.args.get('distance_threshold'))
    df_orderlines = load('df_lines.csv', lines_number)
    df_reswave, df_results = simulation_cluster(y_low, y_high, df_orderlines, list_results, n1, n2, distance_threshold)
    return df_reswave.to_dict()

@app.route('/get-route',methods = ['POST'])
def simulateNBatchOrdersForRoute():
    print(request.args)
    list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = [], [], [], [], [], [], []
    list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]	# Group in list
    # Store Results by Simulation (Order_number)
    list_ordnum , list_dstw = [], []

    lines_number = int(request.args.get('lines_number'))
    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))
    y_low = float(request.args.get('y_low'))
    orderId = request.args.get('orderId')
    y_high = float(request.args.get('y_high'))
    distance_threshold = float(request.args.get('distance_threshold'))
    df_orderlines = load('df_lines.csv', lines_number)
    df_reswave, df_results = simulation_cluster_for_route(y_low, y_high, df_orderlines, list_results, n1, n2, distance_threshold, orderId)
    return df_results.to_dict()

@app.route('/get-route-new',methods = ['POST'])
def simulateNBatchOrdersForRouteSimple():
    print(request.args)
    list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = [], [], [], [], [], [], []
    list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]	# Group in list
    # Store Results by Simulation (Order_number)
    list_ordnum , list_dstw = [], []

    lines_number = int(request.args.get('lines_number'))
    n1 = int(request.args.get('n1'))
    n2 = int(request.args.get('n2'))
    y_low = float(request.args.get('y_low'))
    y_high = float(request.args.get('y_high'))
    orderId = request.args.get('orderId')
    df_orderlines = load('df_lines.csv', lines_number)
    origin_loc = [0, y_low]
    df_waves, df_results = simulate_batch_route(n1, n2, y_low, y_high, origin_loc, lines_number, df_orderlines, orderId)
    return df_waves.to_dict()


if __name__ == "__main__":
    app.run(debug=True)