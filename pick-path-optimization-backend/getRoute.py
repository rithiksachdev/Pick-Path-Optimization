import pandas as pd
import numpy as np 
import itertools
from ast import literal_eval
from scipy.cluster.vq import kmeans2, whiten
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import ward, fcluster

def cluster_locations(list_coord, distance_threshold, dist_method, clust_start):
    ''' Step 1: Create clusters of locations'''
    # Create linkage matrix
    if dist_method == 'euclidian':
        Z = ward(pdist(np.stack(list_coord)))
    else:
        Z = ward(pdist(np.stack(list_coord), metric = distance_picking_cluster))
    # Single cluster array
    fclust1 = fcluster(Z, t = distance_threshold, criterion = 'distance')
    return fclust1


def clustering_mapping(df, distance_threshold, dist_method, orders_number, wave_start, clust_start, df_type): # clustering_loc
    '''Step 2: Clustering and mapping'''
    # 1. Create Clusters
    list_coord, list_OrderNumber, clust_id, df = cluster_wave(df, distance_threshold, 'custom', clust_start, df_type)
    clust_idmax = max(clust_id) # Last Cluster ID
    # 2. Mapping Order lines
    dict_map, dict_omap, df, Wave_max = lines_mapping_clst(df, list_coord, list_OrderNumber, clust_id, orders_number, wave_start)
    return dict_map, dict_omap, df, Wave_max, clust_idmax


def cluster_wave(df, distance_threshold, dist_method, clust_start, df_type):
    '''Step 3: Create waves by clusters'''
    # Create Column for Clustering
    if df_type == 'df_mono':
        df['Coord_Cluster'] = df['Coord'] 
    # Mapping points
    df_map = pd.DataFrame(df.groupby(['OrderNumber', 'Coord_Cluster'])['SKU'].count()).reset_index() 	# Here we use Coord Cluster
    list_coord, list_OrderNumber = np.stack(df_map.Coord_Cluster.apply(lambda t: literal_eval(t)).values), df_map.OrderNumber.values
    # Cluster picking locations
    clust_id = cluster_locations(list_coord, distance_threshold, dist_method, clust_start)
    clust_id = [(i + clust_start) for i in clust_id]
    # List_coord
    list_coord = np.stack(list_coord)
    return list_coord, list_OrderNumber, clust_id, df


def lines_mapping(df, orders_number, wave_start):
    '''Step 4: Mapping Order lines mapping without clustering '''
    # Unique order numbers list
    list_orders = df.OrderNumber.unique()
    # Dictionnary for mapping
    dict_map = dict(zip(list_orders, [i for i in range(1, len(list_orders))]))
    # Order ID mapping
    df['OrderID'] = df['OrderNumber'].map(dict_map)
    # Grouping Orders by Wave of orders_number 
    df['WaveID'] = (df.OrderID%orders_number == 0).shift(1).fillna(0).cumsum() + wave_start
    # Counting number of Waves
    waves_number = df.WaveID.max() + 1
    return df, waves_number


def lines_mapping_clst(df, list_coord, list_OrderNumber, clust_id, orders_number, wave_start):
    '''Step 4: Mapping Order lines mapping with clustering '''
    # Dictionnary for mapping by cluster
    dict_map = dict(zip(list_OrderNumber, clust_id))
    # Dataframe mapping
    df['ClusterID'] = df['OrderNumber'].map(dict_map)
    # Order by ID and mapping
    df = df.sort_values(['ClusterID','OrderNumber'], ascending = True)
    list_orders = list(df.OrderNumber.unique())
    # Dictionnary for order mapping 
    dict_omap = dict(zip(list_orders, [i for i in range(1, len(list_orders))]))
    # Order ID mapping
    df['OrderID'] = df['OrderNumber'].map(dict_omap)
    # Create Waves: Increment when reaching orders_number or changing cluster
    df['WaveID'] = wave_start + ((df.OrderID%orders_number == 0) | (df.ClusterID.diff() != 0)).shift(1).fillna(0).cumsum() 

    wave_max = df.WaveID.max()
    return dict_map, dict_omap, df, wave_max


def locations_listing(df_orderlines, wave_id):
    ''' Step 5: Listing location per Wave of orders'''

    # Filter by wave_id
    df = df_orderlines[df_orderlines.WaveID == wave_id]
    # Create coordinates listing
    list_coord = list(df['Coord'].apply(lambda t: literal_eval(t)).values) 	# Here we use Coord for distance
    list_coord.sort()
    # Get unique Unique coordinates
    list_coord = list(k for k,_ in itertools.groupby(list_coord))
    n_locs = len(list_coord)
    n_lines = len(df)
    n_pcs = df.PCS.sum()

    return list_coord, n_locs, n_lines, n_pcs

def simulation_wave(y_low, y_high, orders_number, df_orderlines, list_results, distance_threshold, mono_method, multi_method, orderId):
    ''' Simulate the distance for a number of orders per wave'''
    # List to store values
    [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult] = [list_results[i] for i in range(len(list_results))]

    # Variables to store total distance
    distance_route = 0
    origin_loc = [0, y_low] 	
    # Mapping of orderlines with waves number
    df_orderlines, waves_number = df_mapping(df_orderlines, orders_number, distance_threshold, mono_method, multi_method)
    df_o = df_orderlines.loc[df_orderlines.OrderNumber == int(orderId), :]
    wave_id = df_o.iloc[0].WaveID
    print(wave_id)
    # Loop
    df_orders = (df_orderlines.loc[df_orderlines.WaveID == wave_id])

    orderNumberList = df_orders['OrderNumber'].tolist()
    # Listing of all locations for this wave 
    list_locs, n_locs, n_lines, n_pcs = locations_listing(df_orderlines, wave_id)
    # Create picking route
    wave_distance, list_chemin, distance_max = create_picking_route_cluster(origin_loc, list_locs, y_low, y_high)

    print(list_chemin)
    
    # Total walking distance
    distance_route = distance_route + wave_distance
    # Results by wave
    monomult = mono_method + '-' + multi_method

    # Add the results 
    list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = append_results(list_wid, list_dst, list_route, list_ord, list_lines, 
    list_pcs, list_monomult, wave_id, wave_distance, list_chemin, orders_number, n_lines, n_pcs, monomult, orderNumberList)

    # List results
    list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]
    return list_results, distance_route


def loop_wave(y_low, y_high, df_orderlines, list_results, n1, n2, distance_threshold, mono_method, multi_method, orderId):
    ''' Simulate all scenarios for each number of orders per wave'''
    # Lists for records
    list_ordnum, list_dstw = [], []
    lines_number = len(df_orderlines)
    # Test several values of orders per wave
    for orders_number in range(n1, n2):
        # Scenario of orders/wave = orders_number 
        list_results, distance_route = simulation_wave(y_low, y_high, orders_number, df_orderlines, list_results,
            distance_threshold, mono_method, multi_method, orderId)
        # Append results per Wave
        list_ordnum.append(orders_number)
        list_dstw.append(distance_route)
        print("{} orders/wave: {:,} m".format(orders_number, distance_route))
    # Output list
    [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult] = [list_results[i] for i in range(len(list_results))]
    # Output results per wave
    df_results, df_reswave = create_dataframe(list_wid, list_dst, list_route, list_ord, 
        distance_route, list_lines, list_pcs, list_monomult, list_ordnum, list_dstw)
    return list_results, df_reswave


def simulation_cluster_for_route(y_low, y_high, df_orderlines, list_results, n1, n2, distance_threshold, orderId):
    '''Simulate for three scenarios'''
    # Loop_wave: Simulation 1
    mono_method, multi_method = 'normal', 'normal'
    list_results, df_reswave1 = loop_wave(y_low, y_high, df_orderlines, list_results, n1, n2, 
        distance_threshold, mono_method, multi_method, orderId)
    # Loop_wave: Simulation 2
    mono_method, multi_method = 'clustering', 'normal'
    list_results, df_reswave2 = loop_wave(y_low, y_high, df_orderlines, list_results, n1, n2, 
        distance_threshold, mono_method, multi_method, orderId)
    # Loop_wave: Simulation 3
    mono_method, multi_method = 'clustering', 'clustering'
    list_results, df_reswave3 = loop_wave(y_low, y_high, df_orderlines, list_results, n1, n2, 
        distance_threshold, mono_method, multi_method, orderId)

    # Expand
    [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult] = [list_results[i] for i in range(len(list_results))]
    lines_number = len(df_orderlines)

    # Results 
    df_results = pd.DataFrame({'wave_number': list_wid,
                                'distance': list_dst,
                                'chemins': list_route,
                                'order_per_wave': list_ord,
                                'lines': list_lines,
                                'pcs': list_pcs,
                                'mono_multi':list_monomult})
                                
    # Final Processing
    print("FINALLL")
    print(df_results['chemins'])
    df_reswave = process_methods(df_reswave1, df_reswave2, df_reswave3, lines_number, distance_threshold)

    return df_reswave, df_results


def create_dataframe(list_wid, list_dst, list_route, list_ord, distance_route, list_lines, list_pcs, list_monomult, list_ordnum, list_dstw):
    ''' Create Dataframes of results'''

    # Results by Wave df
    df_results = pd.DataFrame({'wave_number': list_wid,
                                'distance': list_dst,
                                'chemin': list_route,
                                'orders_per_wave': list_ord,
                                'lines': list_lines,
                                'pcs': list_pcs,
                                'mono_multi':list_monomult})
    # Results by Wave_ID
    df_reswave = pd.DataFrame({
        'orders_number': list_ordnum,
        'distance': list_dstw 
        })

    return df_results, df_reswave

# Append Results
def append_results(list_wid, list_dst, list_route, list_ord, list_lines, 
		list_pcs, list_monomult, wave_id, wave_distance, list_chemin, orders_number, n_lines, n_pcs, monomult, orderNumberList):

	list_wid.append(wave_id)
	list_dst.append(wave_distance)
	list_route.append(list_chemin)
	list_ord.append(orders_number)
	list_lines.append(n_lines)
	list_pcs.append(orderNumberList)
	list_monomult.append(monomult)

	return list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult


def process_methods(df_reswave1, df_reswave2, df_reswave3, lines_number, distance_threshold):
    ''' Process the results of three methods'''

    # Concatenate two dataframes for plot
    df_reswave1.rename(columns={"distance": "distance_method_1"}, inplace = True)
    df_reswave2.rename(columns={"distance": "distance_method_2"}, inplace = True)
    df_reswave3.rename(columns={"distance": "distance_method_3"}, inplace = True)

    df_reswave = df_reswave1.set_index('orders_number')
    # Rename columns
    df_reswave['distance_method_2'] = df_reswave2.set_index('orders_number')['distance_method_2']
    df_reswave['distance_method_3'] = df_reswave3.set_index('orders_number')['distance_method_3']

    # df_reswave.reset_index().plot.bar(x = 'orders_number', y = ['distance_method_1', 'distance_method_2', 'distance_method_3'], 
    #     figsize=(10, 6), color = ['black', 'red', 'blue'])


    return df_reswave

def df_mapping(df_orderlines, orders_number, distance_threshold, mono_method, multi_method):
    ''' Mapping Order lines Dataframe using clustering'''
    # Filter mono and multi orders
    df_mono, df_multi = process_lines(df_orderlines)
    wave_start = 0
    clust_start = 0

    # Mapping for single line orders
    if mono_method == 'clustering':		
        df_type = 'df_mono' 	
        dict_map, dict_omap, df_mono, waves_number, clust_idmax = clustering_mapping(df_mono, distance_threshold, 'custom', 
            orders_number, wave_start, clust_start, df_type)
    else: 
        df_mono, waves_number = lines_mapping(df_mono, orders_number, 0)
        clust_idmax = 0 
        # => Wave_start
    wave_start = waves_number
    clust_start = clust_idmax 

    # Mapping for multi line orders
    if multi_method == 'clustering':
        df_type = 'df_multi' 	
        df_multi = centroid_mapping(df_multi)
        dict_map, dict_omap, df_multi, waves_number, clust_idmax  = clustering_mapping(df_multi, distance_threshold, 'custom', 
            orders_number, wave_start, clust_start, df_type)
    else:
        df_multi, waves_number = lines_mapping(df_multi, orders_number, wave_start)

    # Final Concatenation
    df_orderlines, waves_number = monomult_concat(df_mono, df_multi)

    return df_orderlines, waves_number

# Calculate total distance to cover for a list of locations
def create_picking_route_cluster(origin_loc, list_locs, y_low, y_high):
    # Total distance variable
    wave_distance = 0
    # Distance max
    distance_max = 0
    # Current location variable 
    start_loc = origin_loc
    # Store routes
    list_chemin = []
    list_chemin.append(start_loc)
    while len(list_locs) > 0: # Looping until all locations are picked
        # Going to next location
        list_locs, start_loc, next_loc, distance_next = next_location(start_loc, list_locs, y_low, y_high)
        # Update start_loc 
        start_loc = next_loc
        list_chemin.append(start_loc)
        if distance_next > distance_max:
            distance_max = distance_next
        # Update distance
        wave_distance = wave_distance + distance_next 
    # Final distance from last storage location to origin
    wave_distance = wave_distance + distance_picking(start_loc, origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)
    return wave_distance, list_chemin, distance_max


def distance_picking(Loc1, Loc2, y_low, y_high):
    '''Calculate Picker Route Distance between two locations'''
	# Start Point
    x1, y1 = Loc1[0], Loc1[1]
    # End Point
    x2, y2 = Loc2[0], Loc2[1]
    # Distance x-axis
    distance_x = abs(x2 - x1)
    # Distance y-axis
    if x1 == x2:
        distance_y1 = abs(y2 - y1)
        distance_y2 = distance_y1
    else:
        distance_y1 = (y_high - y1) + (y_high - y2)
        distance_y2 = (y1 - y_low) + (y2 - y_low)
    # Minimum distance on y-axis 
    distance_y = min(distance_y1, distance_y2)
    # Total distance
    distance = distance_x + distance_y
    return int(distance)

def next_location(start_loc, list_locs, y_low, y_high):
    '''Find closest next location'''
    # Distance to every next points candidate
    list_dist = [distance_picking(start_loc, i, y_low, y_high) for i in list_locs]
    # Minimum Distance 
    distance_next = min(list_dist)
    # Location of minimum distance
    index_min = list_dist.index(min(list_dist))
    next_loc = list_locs[index_min] 
    list_locs.remove(next_loc) 
    return list_locs, start_loc, next_loc, distance_next


def centroid(list_in):
    '''Centroid function'''
    x, y = [p[0] for p in list_in], [p[1] for p in list_in]
    centroid = [round(sum(x) / len(list_in),2), round(sum(y) / len(list_in), 2)]
    return centroid

 
def centroid_mapping(df_multi):
    '''Mapping Centroids'''
    # Mapping multi
    df_multi['Coord'] = df_multi['Coord'].apply(literal_eval)
    # Group coordinates per order
    df_group = pd.DataFrame(df_multi.groupby(['OrderNumber'])['Coord'].apply(list)).reset_index()
    # Calculate Centroid
    df_group['Coord_Centroid'] = df_group['Coord'].apply(centroid)
    # Dictionnary for mapping
    list_order, list_coord = list(df_group.OrderNumber.values), list(df_group.Coord_Centroid.values)
    dict_coord = dict(zip(list_order, list_coord))
    # Final mapping
    df_multi['Coord_Cluster'] = df_multi['OrderNumber'].map(dict_coord).astype(str)
    df_multi['Coord'] = df_multi['Coord'].astype(str)
    return df_multi

def distance_picking_cluster(point1, point2):

    y_low, y_high = 5.5, 50 
    # Start Point
    x1, y1 = point1[0], point1[1]
    # End Point
    x2, y2 = point2[0], point2[1]
    # Distance x-axis
    distance_x = abs(x2 - x1)
    # Distance y-axis
    if x1 == x2:
        distance_y1 = abs(y2 - y1)
        distance_y2 = distance_y1
    else:
        distance_y1 = (y_high - y1) + (y_high - y2)
        distance_y2 = (y1 - y_low) + (y2 - y_low)
    # Minimum distance on y-axis 
    distance_y = min(distance_y1, distance_y2)
    # Total distance
    distance = distance_x + distance_y
    return distance

def process_lines(df_orderlines):
    ''' Processing of dataframe '''
    # Mapping Order lines
    df_nline = pd.DataFrame(df_orderlines.groupby(['OrderNumber'])['SKU'].count())

    # Lists
    list_ord = list(df_nline.index.astype(int).values)
    list_lines = list(df_nline['SKU'].values.astype(int))

    # Mapping
    dict_nline = dict(zip(list_ord, list_lines))
    df_orderlines['N_lines'] = df_orderlines['OrderNumber'].map(dict_nline)

    # Processing
    df_mono, df_multi = df_orderlines[df_orderlines['N_lines'] == 1], df_orderlines[df_orderlines['N_lines'] > 1]
    del df_orderlines

    return df_mono, df_multi

def monomult_concat(df_mono, df_multi):
    ''' Concat mono-line and multi-lines orders'''
    # Original Coordinate for mono 
    df_mono['Coord_Cluster'] = df_mono['Coord']
    # Dataframe Concatenation
    df_orderlines = pd.concat([df_mono, df_multi])
    # Counting number of Waves
    waves_number = df_orderlines.WaveID.max() + 1

    return df_orderlines, waves_number