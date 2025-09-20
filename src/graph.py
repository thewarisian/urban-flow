class Graph:
    #Class counter variable to generate numbers for default names of new nodes
    latest_node_num = 1

    def __init__(self):
        #Key: Node name, Value: Set of names of nodes to which given node is linked in graph
        self.adjacency_list = {}

    def __contains__(self, 
                     node_name:str):
        #List of names of all nodes in graph
        all_node_names = self.adjacency_list.keys()

        #Return whether node to be checked is within list of all node names
        return node_name in all_node_names
    
    def __iter__(self):
        #Return the iterator of the 'adjacency_list' dict wrapped within the graph object
        return iter(self.adjacency_list)

    def add_node(self, 
                 new_node_name:str=f"Node {latest_node_num}", 
                 new_node_connections:set[str]=None) -> None:
        """
        Add a new node to the graph.

        Parameters
        ----------
        new_node_name : str
            Name of the node to add. If no value passed, generates a default name".
        new_node_connections : set of str, optional
            List of names of nodes to connect this node to. Defaults to an empty list.

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
        
        #Creates new empty list reference if no connections provided for new node
        if new_node_connections is None:
            new_node_connections = set()
        
        #Check to ensure all nodes named as connections to this new node actually exist in the graph
        all_node_names = set(self.adjacency_list.keys())
        if not new_node_connections <= all_node_names:
            extra_nodes = new_node_connections - all_node_names
            raise ValueError(f"Node(s) named '{extra_nodes}' do not exist in graph.")
        
        #Update counter for generating default names for new nodes
        Graph.latest_node_num += 1
            
        #Add node if not already present
        self.adjacency_list[new_node_name] = new_node_connections
    
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
        del self.adjacency_list[deleted_node_name]

        #Delete all mentions in adjacency lists of remaining nodes
        for node in self:
            self.adjacency_list[node].discard(deleted_node_name)

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
        
        #Store list of all nodes connected to node that is going to be deleted
        node_adjacencies = self.adjacency_list.pop(old_node_name) 

        #Adding node with exact same connections as previous node, but with the new name
        self.add_node(new_node_name, node_adjacencies)

        #Replace all mentions in adjacency lists of remaining nodes with new name
        for node in self:
            if old_node_name in self.adjacency_list[node]:
                self.adjacency_list[node].discard(old_node_name)
                self.adjacency_list[node].add(new_node_name)
