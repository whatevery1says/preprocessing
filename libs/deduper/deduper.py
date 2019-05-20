#!/usr/bin/env python3
"""
First it filters the data by weight.
From the data, it builds a links dictionary, src -> dst.
From the links, it builds a list of complete graphs -- articles which are all duplicates of one another, and not duplicates of anything else.
"""

import itertools

test_links = [
        # single duplicate listing
        ['single.a', 'single.b'],

        # double duplicate listing
        ['double.a', 'double.b'],
        ['double.b', 'double.a'],

        # self-duplicate (bad data)
        ['self.a', 'self.a'],

        # a complete graph
        ['complete.a', 'complete.b'],
        ['complete.b', 'complete.c'],
        ['complete.c', 'complete.a'],

        # # a chain with a shared duplicate
        ['chain.a', 'chain.ab'],
        ['chain.ab', 'chain.b'],

        # a complex graph -- diamond
        ['cx1.WEST', 'cx1.NORTH'],
        ['cx1.WEST', 'cx1.SOUTH'],
        ['cx1.EAST', 'cx1.NORTH'],
        ['cx1.EAST', 'cx1.SOUTH'],

        # a complex graph -- two triangles with a shared point
        ['cx2.A1', 'cx2.A2'],
        ['cx2.A2', 'cx2.SHARE'],
        ['cx2.A1', 'cx2.SHARE'],
        ['cx2.B1', 'cx2.B2'],
        ['cx2.B2', 'cx2.SHARE'],
        ['cx2.B1', 'cx2.SHARE'],
        ]


def filter_pairs_by_values(seq, values):
    """"""
    for el in seq:
        if el[0] not in values and el[1] not in values:
            yield el


def filter_triples_by_threshold(seq, threshold):
    """"""
    for el in seq:
        if el[0] > threshold:
            yield [el[1], el[2]]


class LinkFilter:
    """LinkFilter loads a list of links (optionally filtered by score),
    and computes filtered lists of edges or nodes base on two criteria"""
    
    # In the future could be implemented using a graph library like NetworkX
    # https://stackoverflow.com/questions/15644684/best-practices-for-querying-graphs-by-edge-and-node-attributes-in-networkx
    
    def __init__(self, links_data=[]):
        """Initialize the LinkFilter with a link list."""
        self.clear()
        self._links = links_data

    # def append_weighted_links(self, links_data, threshold):
    #     """Given links with scores, filter by score and append filtered links.
    #     Designed for FuzzyHasher ssdeep score output.
    #     """
    #     for score, node_a, node_b in links_data:
    #         if score > threshold:
    #             self._links.append([node_a, node_b])

    def clear(self):
        """Clear all cached values. Removes invalid results after
        modifying links list."""
        self._links = []
        self._links_dict = {}
        self._neighborhoods = {}
        self._leaves = []
        self._components = set()
        self._complete = set()

    @property
    def links(self):
        """A list of links. Each link is a pair of elements [node_a, node_b]."""
        return self._links

    @links.setter
    def links(self, links_data):
        """Setter for links. Link rows must be [node,node] or [score, node, node] Given links with scores, filter by score and append filtered links.
    #     Designed for FuzzyHasher ssdeep score output.
"""
        self.clear()
        if links_data:
            columns = len(links_data[0])
            if columns == 2:
                self._links = links_data
            elif columns >= 3:
                for item in links_data:
                    self._links.append([item[1], item[2]])
            else:
                raise IndexError("link rows must be node-node or score-node-node.")

    @property
    def links_dict(self):
        """A dictionary of nodes, each with a set of its links.
        Links [[a,b],[b,c]] will create dictionary {a:{b}, b:{a,c}, c:{b}}
        """
        if not self._links_dict:
            if not self._links:
                return None
            self._links_dict = {}
            for src, dst in self.links:
                if src != dst:
                    if src in self._links_dict:
                        self._links_dict[src].add(dst)
                    else:
                        self._links_dict[src] = set([dst])
                    if dst in self._links_dict:
                        self._links_dict[dst].add(src)
                    else:
                        self._links_dict[dst] = set([src])
            # print("\nlinks_dict:\n", links_dict, "\n")
        return self._links_dict
    
    @links_dict.setter
    def links_dict(self, links_dict):
        """Setter for links dictionary."""
        self._links_dict = links_dict
    
    # def max_linked_node(self):
    #     max_key = max(links_dict, key=links_dict.get)
    #     print("max_links", max_links)
    #     return max_key

    @property
    def neighborhoods(self):
        """A dictionary of subgraphs generated from the neighborhood
        of each node. Each graph lists the nodes that generate it.
        For example if node 1->2, 2->3, 3->1, 4->5
        then the links contain two neighborhoods: {1, 2, 3} and {4, 5}.
        In the case of non-complete graphs, e.g. A->B->C, there are
        multiple neighborhoods with different node members:
        {{A, B}:A}, {{A, B, C}:B}, {{B, C}:C}.
        """
        if not self._neighborhoods:
            # detect subgraphs exclusive members
            self._neighborhoods = {}
            for key, value in self.links_dict.items():
                temp_graph = value.copy()
                temp_graph.add(key)
                nodegraph = frozenset(temp_graph)
                # print("nodegraph:", nodegraph)
                if nodegraph in self._neighborhoods:
                    self._neighborhoods[nodegraph].add(key)
                else:
                    self._neighborhoods[nodegraph] = set([key])
        # print("\neighborhoods:\n", subgraph_exclusive_members, "\n")
        return self._neighborhoods

    @neighborhoods.setter
    def neighborhoods(self, neighborhoods):
        """Setter for neighborhoods."""
        self._neighborhoods = neighborhoods

    @property
    def leaves(self):
        """"""
        if not self._leaves:
            self._leaves = []
            for key, val in self.neighborhoods.items():
                if len(key)==2 and len(val)==1:
                    for k in key:
                        if k in val:
                            self._leaves.append(k)
        return self._leaves

    @property
    def components(self):
        """A set of disjunct connected components:
        groups of nodes which are linked to each other."""
        if not self._components:
            self._components = set(self.neighborhoods.keys())
            changes = True
            while(changes):
                changes = False
                neighborhood_pairs = itertools.combinations([item for item in self._components], 2)
                for a, b in neighborhood_pairs:
                    if a.issubset(b):
                        try:
                            # print("remove a", a)
                            self._components.remove(a)
                            changes = True
                        except KeyError: # may have already removed this pass
                            pass
                    elif b.issubset(a):
                        try:
                            # print("remove b", b)
                            self._components.remove(b)
                            changes = True
                        except KeyError:
                            pass
                    elif not a.isdisjoint(b):
                        try:
                            # print("remove ab", a, b)
                            self._components.remove(a)
                            self._components.remove(b)
                            self._components.add(a.union(b))
                            changes = False
                        except KeyError:
                            pass
        return self._components

    @components.setter
    def components(self, components):
        """Setter for components."""
        self._components = components

    def is_complete(self, node_list):
        """True if the list of nodes is a complete graph
        (each connected to each) according to their links."""
        if(node_list):
            edges = itertools.combinations([item for item in node_list], 2)
            for node_a, node_b in edges:
                if [node_a, node_b] not in self._links \
                   and [node_b, node_a] not in self._links:
                    # print("missing edge", node_a, node_b)
                    return False
            return True
        return False

    @property
    def complete(self):
        """A set of components which are complete graphs (each to each)."""
        if not self._complete:
            self._complete = set()
            components = self.components.copy()
            for component in components:
                if(self.is_complete(component)):
                    self._complete.add(component)
        return self._complete

    @complete.setter
    def complete(self, complete):
        """Setter for complete graphs."""
        self._complete = complete

    def filter_links(self, source='components', filter='both'):
        """A list of links, filtered by components or complete components.
        When filtered by components, each component removes all nodes but one.
        When filtered by complete, each complete component removes all but one.
        Results may be returned as links to keep, remove, or both."""
        remove_nodes = self.filter_nodes(source, filter='remove')
        keep = []
        remove = []
        for node_a, node_b in self.links:
            if node_a in remove_nodes or node_b in remove_nodes:
                remove.append([node_a, node_b])
            else:
                keep.append([node_a, node_b])
        if filter=='remove':
            return sorted(remove)
        elif filter=='keep':
            return sorted(keep)
        elif filter=='both':
            return { 'keep':sorted(keep), 'remove':sorted(remove) }
        else:
            raise ValueError("filter must be 'keep','remove', or 'both'")

    def filter_nodes(self, source='components', filter='both'):
        """A list of nodes, filtered by components or complete components.
        When filtered by components, each component removes all nodes but one.
        When filtered by complete, each complete component removes all but one.
        Results may be returned as nodes to keep, remove, or both."""
        keep = []
        remove = []
        for component in self.components:
            if source=='components':
                head, *tail = sorted(component)
                for t in tail:
                    remove.append(t)
                keep.append(head)
            elif source=='complete':
                if self.is_complete(component):
                    head, *tail = sorted(component)
                    for t in tail:
                        remove.append(t)
                    keep.append(head)
                else:
                    for item in sorted(component):
                        keep.append(item)
            else:
                raise ValueError("source must be 'components' or 'complete'")
        if filter=='remove':
            return sorted(remove)
        elif filter=='keep':
            return sorted(keep)
        elif filter=='both':
            return { 'keep':sorted(keep), 'remove':sorted(remove) }
        else:
            raise ValueError("filter must be 'keep','remove', or 'both'")
    
    def remove_links(self, source='components'):
        """Remove links based on source strategy."""
        links_to_keep = self.filter_links(source, filter='keep')
        self.links = links_to_keep
        return self.links

    def remove_leaves(self):
        """Remove leaves."""
        leaves = self.leaves
        self.links = list(filter_pairs_by_values(self.links, leaves))
        return leaves

    def __repr__(self):
        """repr for class objects."""
        prstr = self.links or ""
        return(self.__class__.__name__ + "(" + self.links.__str__() + ")")
    
    # def delete_complete(self):
    #     for neighborhood, members in self.neighborhood.items():
    #         if len(neighborhood) == len(members):
    #             # complete subgraphs of size 2/3/4 have only exclusive members.
    #             # Nodes are each linked to each, and other to each other.
    #             # take the first member and delete the others
    #             head, *tail = sorted(members)
    #             self.saves.add(head)
    #             for t in tail:
    #                 self.deletes.add(t)
    #         elif len(neighborhood) == 2 and len(members) == 1:
    #             # terminal nodes in complex groups can be saved and have
    #             # their connecting node marked for deletion
    #                 for d in subgraph.difference(*members):
    #                     deletes.add(d)
    #                 saves.add(*members)
    #         else:
    #             print("Warning! complex subgraph:", subgraph, members)
    #     for d in self.deletes:
    #         if d in self.saves:
    #             self.deletes.remove(d)
    #         links = list(filter_pairs_by_values(links, list(deletes)))

def test():

    ls = LinkFilter(test_links)
    print(ls)
    print('\nlinks:\n', ls.links, '\n')
    print('links_dict:\n', ls.links_dict, '\n')
    print('neighborhoods:\n', ls.neighborhoods, '\n')
    print('leaves\n', ls.leaves, '\n')
    print('components:\n', ls.components, '\n')
    print('complete:\n', ls.complete, '\n')
    
    print('\nFILTERING: components\n')
    
    print('filter nodes (components):\n',
          ls.filter_nodes(source='components'), '\n')
    print('keep nodes (components):\n',
          ls.filter_nodes(source='components', filter='keep'), '\n')
    print('remove nodes (components):\n',
          ls.filter_nodes(source='components', filter='remove'), '\n')
    print('filter links (components):\n',
          ls.filter_links(source='components') ,'\n')
    print('remove links (components):\n',
          ls.remove_links(source='components'), '\n')
    

    print('\nFILTERING: complete\n')

    ls.links = test_links
    
    print('filter nodes (complete):\n',
          ls.filter_nodes(source='complete'), '\n')
    print('keep nodes (complete):\n',
          ls.filter_nodes(source='complete', filter='keep'), '\n')
    print('remove nodes (complete):\n',
          ls.filter_nodes(source='complete', filter='remove'), '\n')
    print('filter links (complete):\n',
          ls.filter_links(source='complete'), '\n')
    print('remove links (complete):\n',
          ls.remove_links(source='complete'), '\n')

    print('\nFILTERING: leaves\n')

    ls.links = test_links
    print('remove leaves:\n', ls.remove_leaves(), '\n', ls.links, '\n')
    print('filter nodes (components):\n',
          ls.filter_nodes(source='components'), '\n')
    

test()

# # detect pairs
# for key, value in links_dict.items():
#     if len(value) == 1:
#         only_value = next(iter(value))
#         if len(links_dict[only_value]) == 1:
#             if key not in deletes:
#                 deletes.append(only_value)
#                 saves.append
#                 print('pair', key, value)

