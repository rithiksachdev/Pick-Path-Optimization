import pandas as pd
import numpy as np 
import itertools
from ast import literal_eval


def orderlines_mapping(df_orderlines, orders_number):
    '''Mapping orders with wave number'''
    df_orderlines.sort_values(by='DATE', ascending = True, inplace = True)
    # Unique order numbers list
    list_orders = df_orderlines.OrderNumber.unique()
    dict_map = dict(zip(list_orders, [i for i in range(1, len(list_orders))]))
    # Order ID mapping
    df_orderlines['OrderID'] = df_orderlines['OrderNumber'].map(dict_map)
    # Grouping Orders by Wave of orders_number 
    df_orderlines['WaveID'] = (df_orderlines.OrderID%orders_number == 0).shift(1).fillna(0).cumsum()
    # Counting number of Waves
    waves_number = df_orderlines.WaveID.max() + 1
    return df_orderlines, waves_number

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

def create_picking_route(origin_loc, list_locs, y_low, y_high):
    '''Calculate total distance to cover for a list of locations'''
    # Total distance variable
    wave_distance = 0
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
        # Update distance
        wave_distance = wave_distance + distance_next 

    # Final distance from last storage location to origin
    wave_distance = wave_distance + distance_picking(start_loc, origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)

    return wave_distance, list_chemin


def simulation_wave(y_low, y_high, origin_loc, orders_number, df_orderlines, list_wid, list_dst, list_route, list_ord, orderId):
    ''' Simulate of total picking distance with n orders per wave'''
    distance_route = 0 
    df_orderlines, waves_number = orderlines_mapping(df_orderlines, orders_number)

    df_o = df_orderlines.loc[df_orderlines.OrderNumber == int(orderId), :]
    wave_id = df_o.iloc[0].WaveID
    print(wave_id)
    list_locs, n_locs, n_lines, n_pcs = locations_listing(df_o, wave_id)
    wave_distance, list_chemin = create_picking_route(origin_loc, list_locs, y_low, y_high)
    distance_route = distance_route + wave_distance
    list_wid.append(wave_id)
    list_dst.append(wave_distance)
    list_route.append(list_chemin)
    list_ord.append(orders_number)
    return list_wid, list_dst, list_route, list_ord, distance_route


def simulate_batch_route(n1, n2, y_low, y_high, origin_loc, orders_number, df_orderlines, orderId):
    ''' Loop with several scenarios of n orders per wave'''
    # Lists for results
    list_wid, list_dst, list_route, list_ord = [], [], [], []
    # Test several values of orders per wave

    list_wid, list_dst, list_route, list_ord, distance_route = simulation_wave(y_low, y_high, origin_loc, orders_number, 
    df_orderlines, list_wid, list_dst, list_route, list_ord, orderId)
    print("Total distance covered for {} orders/wave: {:,} m".format(orders_number, distance_route))

    # By Wave
    df_waves = pd.DataFrame({'wave': list_wid,'distance': list_dst,'routes': list_route,'order_per_wave': list_ord})
    print(df_waves)
    # Results aggregate
    df_results = pd.DataFrame(df_waves.groupby(['order_per_wave'])['distance'].sum())
    df_results.columns = ['distance']
    return df_waves, df_results.reset_index()