#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 13:35:16 2021

@author: jiacheng zhu
"""
import random

# custom import
import structured_max_flow 
import func_verify

# define the relevant inputs for a one-source and one-sink network
start_nodes = [1,1,2,2,3,3,4,4,5,5]
end_nodes =   [2,3,3,4,2,5,3,6,4,6]
capacities = [16,13,10,12,4,14,9,20,7,4]
# instance of importance indices class
get_indices = structured_max_flow.ImportanceIndices(start_nodes, end_nodes, capacities)
# run the relevant function
get_indices.One_Source_One_Sink()

# functionality verification of the single-source and single-sink indices
func_verify_single = func_verify.FunctionalityVerification(start_nodes, end_nodes, capacities)
func_verify_single.One_Source_One_Sink(broken_edges_indices=[7])

uncritical_edges=[0, 1,2,4,7,9]
random_attack = random.sample(uncritical_edges, 4)
print(random_attack)
func_verify_single.One_Source_One_Sink(broken_edges_indices=[4])


# define the relevant inputs for a one-source and one-sink network
start_nodes_multi = [1,2,3,3,4,4,5,5,6,6,6,7,7]
start_nodes_multi = [1,2,3,3,4,5,6,7,7,7,8,9,10,11,12,13,14,15,15,16,17,18,19,20,21,22,23,24]
end_nodes_multi =   [4,5,5,6,7,4,4,8,9,10,11,11,13,12,13,14,15,16,21,17,18,19,22,19,20,23,24,25]
capacities_multi = [2800,400,150,100,3450,650,100,500,350,2600,400,250,1800,600,550,2350,2350,350,2000,
                    340,340,335,2335,2000,2000,2330,2330,2330]
multi_source_nodes=[1, 2, 3]
multi_sink_nodes=[25]

# instance of importance indices class
get_indices_multi = structured_max_flow.ImportanceIndices(start_nodes_multi, end_nodes_multi, capacities_multi)
#run the relevant function
get_indices_multi.Multi_Source_Multi_Sink(multi_source_nodes, multi_sink_nodes)


# functionality verification
# instance of functionality verification class
# analysis for critical edges
func_verify_multi = func_verify.FunctionalityVerification(start_nodes_multi, end_nodes_multi, capacities_multi)
func_verify_multi.Multi_Source_Multi_Sink(multi_source_nodes, multi_sink_nodes, broken_edges_indices = [10])

# analysis for not critical edges
start_nodes_multi = [1,2,3,3,4,5,6,7,7,7,8,9,10,11,12,13,14,15,15,16,17,18,19,20,21,22,23,24]
end_nodes_multi =   [4,5,5,6,7,4,4,8,9,10,11,11,13,12,13,14,15,16,21,17,18,19,22,19,20,23,24,25]
capacities_multi = [2800,400,150,100,3450,650,100,500,350,2600,400,250,1800,600,550,2350,2350,350,2000,
                    340,340,335,2335,2000,2000,2330,2330,2330]
multi_source_nodes=[1, 2, 3]
multi_sink_nodes=[25]
func_verify_multi = func_verify.FunctionalityVerification(start_nodes_multi, end_nodes_multi, capacities_multi)
remaning_indices = [0, 1,2,4,5,6,8]
random_choice = random.sample(remaning_indices, 4)
print(random_choice)
func_verify_multi.Multi_Source_Multi_Sink(multi_source_nodes, multi_sink_nodes, broken_edges_indices = [0])
