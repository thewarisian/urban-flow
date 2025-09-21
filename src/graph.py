from typing import Union

class Graph:
    #Class counter variable to generate numbers for default names of new nodes
    latest_node_num = 1

    def __init__(self):
        #Key: Node name, Value: Set of tuples of the form (str, int or float), where the first element is the connected node name and second is the edge weight.
        self.adjacency_list = {}

    def __len__(self):
        #Return the number of nodes in graph, which is the number of keys in the adjacency list dictionary
        return len(self.adjacency_list)
    
    def __contains__(self, 
                     node_name:str):
        #List of names of all nodes in graph
        all_node_names = self.adjacency_list.keys()

        #Return whether node to be checked is within list of all node names
        return node_name in all_node_names
    
    def __iter__(self):
        #Return the iterator of the 'adjacency_list' dict wrapped within the graph object
        return iter(self.adjacency_list)

    def __getitem__(self, key):
        #Access the dictionary around which the graph object is wrapped
        return self.adjacency_list[key]
    
    def __setitem__(self, key, value):
        #Set key, value pair for dictionary around which the graph object is wrapped
        self.adjacency_list[key] = value

    def __delitem__(self, key):
        #Delete the key, value pair from the dictionary around which the graph object is wrapped
        del self.adjacency_list[key]


    def add_node(self, 
                 new_node_name:str=None) -> None:
        """
        Add a new node to the graph.

        Parameters
        ----------
        new_node_name : str
            Name of the node to add. If no value passed, generates a default name".

        Raises
        ------
        ValueError
            If a node with `new_node_name` already exists in the graph.

        Returns
        -------
        None
        """
        #Check to ensure node name doesn't already exist
        if new_node_name in self:
            raise ValueError(f"Node named '{new_node_name}' already exists in graph.")
    
        elif new_node_name is None:
            #Dynamic default name generation
            new_node_name = f"Node {Graph.latest_node_num}"
            #Update counter for generating default names for new nodes
            Graph.latest_node_num += 1
            
        #Add node if not already present
        self[new_node_name] = set()
    
    def delete_node(self, 
                    deleted_node_name:str) -> None:
        """
        Deletes a node from the graph.

        Parameters
        ----------
        deleted_node_name : str
            Name of the node to delete.

        Raises
        ------
        ValueError
            If a node with `deleted_node_name` does not exist in the graph.

        Returns
        -------
        None
        """
        #Checks whether node to be deleted exists in graph
        if deleted_node_name not in self:
            raise ValueError(f"Node named '{deleted_node_name}' does not exist in graph.")
        
        #Delete node if found to be present, collect list of adjacencies
        del self[deleted_node_name]

        #Delete all mentions in adjacency lists of remaining nodes
        for node in self:
            #Creates new dictionary for node where deleted node is excluded
            self[node] = {(name, weight) for (name, weight) in self[node] if name != deleted_node_name}

    def add_edge(self, 
                 from_node_name:str, 
                 to_node_name:str,
                 weight:Union[int, float]=None,
                 undirected_edge:bool=True) -> None:
        """
        Adds an edge between two nodes in a graph. May be weighted or unidirectional.

        Parameters
        ----------
        from_node_name : str
            Name of the node from which added edge emerges.
        to_node_name : str
            Name of the node to which the added edge connects.
        weight : int or float
            Weight assigned to added edge. Unweighted by default.
        undirected_edge : bool
            Whether added edge is unidirectional from 'from_node_name' to 'to_node_name'. Undirected by default.

        Raises
        ------
        ValueError
            If a node with `from_node_name` or 'to_node_name' does not exist in the graph.

        Returns
        -------
        None
        """
        #Checks whether nodes to be linked exist in graph
        if from_node_name not in self:
            raise ValueError(f"Node named '{from_node_name}' does not exist in graph.")
        if to_node_name not in self:
            raise ValueError(f"Node named '{to_node_name}' does not exist in graph.")
        
        #Connect the edges by adding name and weight to the adjacency list
        self[from_node_name].add((to_node_name, weight))

        #If edge is undirected, the same edge is added to the adjacency list in the reverse direction
        if undirected_edge:
            self[to_node_name].add((from_node_name, weight))

    def edge_exists(self, 
                    from_node_name:str, 
                    to_node_name:str,
                    weight:Union[int, float]=None) -> bool:
        """
        Checks if a particular edge exists between two nodes in a graph.

        Parameters
        ----------
        from_node_name : str
            Name of the first node linked by the edge to be searched for.
        to_node_name : str
            Name of the second node linked by the edge to be searched for. 
        weight : int or float
            Weight assigned to edge to be searched for. Unweighted by default.

        Returns
        -------
        True or False
        """
        try:
            #If no weight specified, checks for any edge between given nodes
            if weight is None:
                return any(to_node_name == adjacent_node_name for adjacent_node_name, _ in self[from_node_name])

            #Goes over all nodes listed in adjacency list of first node and returns True if second node is found
            return any((to_node_name, weight) == (adjacent_node_name, adjacent_node_weight) for adjacent_node_name, adjacent_node_weight in self[from_node_name])
        
        except KeyError:
            #Means the node 'from_node_name' doesnt exist in graph
            return False

    def remove_edge(self, 
                    from_node_name:str, 
                    to_node_name:str,
                    weight:Union[int, float]=None,
                    undirected_edge:bool=True) -> None:
        """
        Removes an edge between two nodes in a graph.

        Parameters
        ----------
        from_node_name : str
            Name of the first node linked by the edge to be deleted.
        to_node_name : str
            Name of the second node linked by the edge to be deleted.
        weight : int or float
            Weight assigned to edge to be removed. Considered unweighted by default.
        undirected_edge : bool
            Whether edge to be removed is unidirectional from 'from_node_name' to 'to_node_name'. Undirected by default.

        Raises
        ------
        ValueError
            If no edge exists between nodes `from_node_name` and 'to_node_name' in the graph with the given weight.

        Returns
        -------
        None
        """
        #Checks whether nodes exist and are linked in graph
        if not self.edge_exists(from_node_name, to_node_name, weight):
            error_message = f"No edge exists from {from_node_name} to {to_node_name}."

            #Informs user if there is a directed edge the other way around
            if self.edge_exists(to_node_name, from_node_name, weight):
                error_message += f" Did you mean the edge {to_node_name} -> {from_node_name}?"

            raise ValueError(error_message)
        
        #Removes mentions of linked nodes from adjacency lists of both nodes previously connected by deleted edge
        self[from_node_name] -= {(to_node_name, weight)}
        if undirected_edge:
            self[to_node_name] -= {(from_node_name, weight)}

    def rename_node(self, 
                    old_node_name:str, 
                    new_node_name:str) -> None:
        """
        Renames a particular node in a graph.

        Parameters
        ----------
        old_node_name : str
            Name of the node to be renamed.
        new_node_name : str
            New name of the node to be renamed.

        Raises
        ------
        ValueError
            If a node with `old_node_name` does not exist in the graph.

        Returns
        -------
        None
        """
        #Checks whether node to be deleted exists in graph
        if old_node_name not in self:
            raise ValueError(f"Node named '{old_node_name}' does not exist in graph.")
        
        #Adding node with the new name
        self.add_node(new_node_name)

        #Pops (removes) node with old name and assigns exact same edges to new node with desired name
        self[new_node_name] = self.adjacency_list.pop(old_node_name)

        #Replace all mentions in adjacency lists of remaining nodes with new name
        for node in self:
            #Prevent errors from mutating object dictionary directly
            updated_adjacencies = set()

            #For all edges mentioned in the adjacency list
            for adjacent_node_name, edge_weight in self[node]:
                #If old node name discovered, re add with new name
                if adjacent_node_name == old_node_name:
                    updated_adjacencies.add((new_node_name, edge_weight))
                #Other nodes are added as is
                else:
                    updated_adjacencies.add((adjacent_node_name, edge_weight))

            #New adjacencies added to node
            self[node] = updated_adjacencies
