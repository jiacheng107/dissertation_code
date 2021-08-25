#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 18:15:11 2021

@author:jiacheng zhu
"""

from __future__ import print_function
from ortools.graph import pywrapgraph
import numpy as np
import math
from decimal import Decimal

#use graphviz to visualize the network!!!!!!!


class ImportanceIndices:
    """
    Class to get the component importance indices.

    Attributes:
        LiStartNodes (list): a list of the start nodes for each of the edges in the network
        LiEndNodes (list): a list of the end nodes for each of the edges in the network
        LiCap (list): a list of the capacity on each of the edges in the network
    """

    def __init__(self, LiStartNodes, LiEndNodes, LiCap):
        """
        Initialize ImportanceIndices class.
        Args:
 
        """
        self.LiStartNodes = LiStartNodes
        self.LiEndNodes = LiEndNodes
        self.LiCap = LiCap

    def __del__(self):
        """
        Destructor
        """
        del self.LiStartNodes
        del self.LiEndNodes
        del self.LiCap

    def One_Source_One_Sink(self):
        """
        Function to get the component importance indices for one-source and one-sink netwroks

        """

      # Instantiate a SimpleMaxFlow solver.
        max_flow = pywrapgraph.SimpleMaxFlow()
      # Add each arc.
        for i in range(0, len(self.LiStartNodes)):
            max_flow.AddArcWithCapacity(self.LiStartNodes[i], self.LiEndNodes[i], self.LiCap[i])
     
    #1. for the all pairs max flow edge count
     #define an empty array to store the num of times each arc occurred in a max flow
        times_in_max_flow=np.zeros(max_flow.NumArcs())
      #find the set of all nodes
        all_nodes = self.LiStartNodes + self.LiEndNodes
      #find the set of all unique nodes
        all_unique_nodes = np.unique(np.array(all_nodes))
    
      
      #2. for the edge flow centrality
      #define an empty array to store the sum of flow of each edge on all the max flow pathes
        sum_flow=np.zeros(max_flow.NumArcs())
      #initialize the total flow on all the possible max flow pathes
        all_max_flow=0
      
      #3. for the weighted flow capacity rate
      #3.1 FCR
      
      #4. one-at-a-time damage impact
        one_at_a_time=np.zeros(max_flow.NumArcs())
      #max_flow_before=np.zeros(len(all_unique_nodes)**2 - len(all_unique_nodes))
        change=np.zeros(max_flow.NumArcs())
        WFCR_last= np.zeros(max_flow.NumArcs())
      
        for s in all_unique_nodes:
            for k in all_unique_nodes:
                if s!=k:
                  s=int(s)
                  k=int(k)
                  # Find the maximum flow between node s and node k.
                  if max_flow.Solve(s, k) == max_flow.OPTIMAL:
                    all_max_flow += max_flow.OptimalFlow()
                    #for the one-at-a-time index, record the s-t max flow before change
                    max_flow_before=max_flow.OptimalFlow()
                     #then, define a new max flow problem for the reduced capacity of each esge
                    for i in range(max_flow.NumArcs()):
                        new_capacities = self.LiCap.copy()
                        #print(capacities)
                        #round down the new capacities as capacity should be an integer
                        new_capacities[i] = math.floor(1/2 * self.LiCap[i])
                        #define a new network based on new capacities (maybe define a function for this)
                        max_flow2=pywrapgraph.SimpleMaxFlow()
                        for j in range(0, len(self.LiStartNodes)):
                            max_flow2.AddArcWithCapacity(self.LiStartNodes[j], self.LiEndNodes[j], new_capacities[j])
                        if max_flow2.Solve(s, k) == max_flow2.OPTIMAL:
                            max_flow_after=max_flow2.OptimalFlow()
                        if max_flow_before != 0:
                            change[i]+=(max_flow_before-max_flow_after)/max_flow_before
                        
                    for i in range(max_flow.NumArcs()):
                      sum_flow[i]+= max_flow.Flow(i)
                      if max_flow.Flow(i)!=0:
                          times_in_max_flow[i]+=1
                          
                      # for the weighted FCR
                      WFCR_last[i] += (max_flow.Flow(i) **2) /self.LiCap[i]
                  else:
                    print('There was an issue with the max flow input.')
                    
        all_pairs_max_flow_edge_count_index = np.array(times_in_max_flow/(len(all_unique_nodes)*(len(all_unique_nodes)-1)))
        edge_flow_centrality_index = np.array(sum_flow/all_max_flow)
        one_at_a_time_damage_impact_index = np.array(change/(len(all_unique_nodes)*(len(all_unique_nodes)-1)))
        WFCR_index = np.array(WFCR_last/ (len(all_unique_nodes)*(len(all_unique_nodes)-1) * all_max_flow))
      
      # get the average index
      #first, Concatenate the obtained arrays
        concate_array = np.vstack((all_pairs_max_flow_edge_count_index, edge_flow_centrality_index,one_at_a_time_damage_impact_index, WFCR_index))
      #check if the concatenate is done correctly
        #print(concate_array.shape)
      #compute the average index for each edge
        average_index = np.mean(concate_array, axis=0)
      
    
        print('all pairs max flow edge count index: ', np.round(all_pairs_max_flow_edge_count_index, 3))
        print('edge flow centrality index: ', np.round(edge_flow_centrality_index, 3))
        print('one-at-a-time damage impact index: ', np.round(one_at_a_time_damage_impact_index, 3))
        print('the weighted flow capacity rate index: ', np.round(WFCR_index, 3)) 
        print('the average index is: ', np.round(average_index, 3))
  
  
  
  
  #5. for multi-source and multi-sink (referring to another paper )
#  the centrality index
# here,don't walk through all the nodes for s-t but focus on the true s nodes and t nodes in the network

    def Multi_Source_Multi_Sink(self, multi_source_nodes, multi_sink_nodes):
        """
        Function to get the component importance index for multi-source and multi-sink netwroks
        
        Arg:
            multi_source_nodes (list): a list of the multiple source nodes
            multi_sink_noodes (list): a list of multiple sink nodes
            
        Return:
            the corresponding index values
            
        """ 
    # Instantiate a SimpleMaxFlow solver.
        max_flow_multi = pywrapgraph.SimpleMaxFlow()
  # Add each arc.
        for i in range(0, len(self.LiStartNodes)):
            max_flow_multi.AddArcWithCapacity(self.LiStartNodes[i], self.LiEndNodes[i], self.LiCap[i])
    
  #need to pre-define the source nodes and sink nodes according to the network
        try:
            multi_source_nodes = multi_source_nodes
        except Exception as e:
            print('Exception encountered during predictions: ',e)
            print('Perhaps you forgot to enter the multiple source nodes???')
      
        try:
            multi_sink_nodes = multi_sink_nodes
        except Exception as e:
            print('Exception encountered during predictions: ',e)
            print('Perhaps you forgot to enter the multiple sink nodes???')
      
  #define an empty array to store the sum of flow of each edge on all the max flow pathes
        sum_flow_multi=np.zeros(max_flow_multi.NumArcs())
  #initialize a sum of all the possible max flow
        all_max_flow_multi =0 
      
        for s in multi_source_nodes:
            for k in multi_sink_nodes:
                s=int(s)
                k=int(k)
              # Find the maximum flow between node s and node k.
                if max_flow_multi.Solve(s, k) == max_flow_multi.OPTIMAL:
                    all_max_flow_multi += max_flow_multi.OptimalFlow()
                    for i in range(max_flow_multi.NumArcs()):
                      sum_flow_multi[i]+= max_flow_multi.Flow(i)              
                else:
                    print('There was an issue with the max flow input.')
        
        centrality_index = sum_flow_multi/all_max_flow_multi
        print('centrality index of multi-source and multi-sink network is: ', np.round(centrality_index, 2))

