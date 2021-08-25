#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 15:37:24 2021
@author: jiacheng zhu

"""

from __future__ import print_function
from ortools.graph import pywrapgraph
import numpy as np
import math

#use graphviz to visualize the network!!!!!!!


class FunctionalityVerification:
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
 
  # for multi-source and multi-sink (referring to another paper )
#  the centrality index
# here,don't walk through all the nodes for s-t but focus on the true s nodes and t nodes in the network

    def Multi_Source_Multi_Sink(self, multi_source_nodes, multi_sink_nodes, broken_edges_indices = None):
        """
        Function to get the component importance index for multi-source and multi-sink netwroks
        
        Arg:
            multi_source_nodes (list): a list of the multiple source nodes
            multi_sink_noodes (list): a list of multiple sink nodes
            broken_edges_indices (list): a list of the index of the broken edges due to a disruption
            
        Return:
            the correspondingmax flow capacity of the current network
            
        """ 
        
    # make a copy of the capacity list to work with
        cap_copy = self.LiCap.copy()
    # set the capacity of the broken edges as 50% of original one if there is any
        if broken_edges_indices:
            for index in broken_edges_indices:
                cap_copy[index] = math.floor(0.5 * cap_copy[index])
    # Instantiate a SimpleMaxFlow solver.
        max_flow_multi = pywrapgraph.SimpleMaxFlow()
        
        max_flow_multi_damage = pywrapgraph.SimpleMaxFlow()
  # Add each arc.
        for i in range(0, len(self.LiStartNodes)):
            max_flow_multi.AddArcWithCapacity(self.LiStartNodes[i], self.LiEndNodes[i], self.LiCap[i])
            max_flow_multi_damage.AddArcWithCapacity(self.LiStartNodes[i], self.LiEndNodes[i], cap_copy[i])
    
  # need to pre-define the source nodes and sink nodes according to the network
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
      
  # define an empty array to store the sum of flow of each edge on all the max flow pathes
        sum_flow_multi=np.zeros(max_flow_multi.NumArcs())
  # initialize a sum of all the possible max flow
        all_max_flow_multi =0 
        all_max_flow_damage = 0
      
        for s in multi_source_nodes:
            for k in multi_sink_nodes:
                s=int(s)
                k=int(k)
              # Find the maximum flow between node s and node k.
                if max_flow_multi.Solve(s, k) == max_flow_multi.OPTIMAL:
                    all_max_flow_multi += max_flow_multi.OptimalFlow()
                    
                if max_flow_multi_damage.Solve(s, k) == max_flow_multi_damage.OPTIMAL:
                    all_max_flow_damage += max_flow_multi_damage.OptimalFlow()               
                else:
                    print('There was an issue with the max flow input.')
        print('the max flow capacity is: ', all_max_flow_multi)
        print('the max flow capacity decreases to its {} percentage due to the attack'.format(np.round(all_max_flow_damage/all_max_flow_multi, 4)*100))
        
        

    def One_Source_One_Sink(self, broken_edges_indices = None):
        """
        Function to get the component importance indices for one-source and one-sink netwroks

        """
    # make a copy of the capacity list to work with
        cap_copy = self.LiCap.copy()
    # set the capacity of the broken edges as 50% of original one if there is any
        if broken_edges_indices:
            for index in broken_edges_indices:
                cap_copy[index] = math.floor(0.5 * cap_copy[index])
                
      # Instantiate a SimpleMaxFlow solver for the original network.
        max_flow = pywrapgraph.SimpleMaxFlow()
      # Instantiate a SimpleMaxFlow solver for the attacked network.
        max_flow_damage = pywrapgraph.SimpleMaxFlow()
      # Add each arc.
        for i in range(0, len(self.LiStartNodes)):
            max_flow.AddArcWithCapacity(self.LiStartNodes[i], self.LiEndNodes[i], self.LiCap[i])
            max_flow_damage.AddArcWithCapacity(self.LiStartNodes[i], self.LiEndNodes[i], cap_copy[i])
            

              #find the set of all nodes
        all_nodes = self.LiStartNodes + self.LiEndNodes
      #find the set of all unique nodes
        all_unique_nodes = np.unique(np.array(all_nodes))
        
        # declare a max flow capacity in the original network
        all_max_flow = 0
        # declare a max flow capacity in the attacked network
        all_max_flow_damage = 0
      
        for s in all_unique_nodes:
            for k in all_unique_nodes:
                if s!=k:
                  s=int(s)
                  k=int(k)
                  # Find the maximum flow between node s and node k.
                  if max_flow.Solve(s, k) == max_flow.OPTIMAL:
                    all_max_flow += max_flow.OptimalFlow()   
                  if max_flow_damage.Solve(s, k) == max_flow_damage.OPTIMAL:
                    all_max_flow_damage += max_flow_damage.OptimalFlow()
                  else:
                    print('There was an issue with the max flow input.')
                    
        print('the max flow capacity decreases to its {} percentage due to the attack'.format(np.round(all_max_flow_damage/all_max_flow, 4)*100))
                    

