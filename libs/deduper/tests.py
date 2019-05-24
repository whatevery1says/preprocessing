#!/usr/bin/env python3

import unittest
from deduper import LinkFilter

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

test_links_scores = [
        # single duplicate listing
        ['80', 'single.a', 'single.b'],

        # double duplicate listing
        ['72', 'double.a', 'double.b'],
        ['72', 'double.b', 'double.a'],

        # self-duplicate (bad data)
        ['100', 'self.a', 'self.a'],

        # a complete graph
        ['60', 'complete.a', 'complete.b'],
        ['70', 'complete.b', 'complete.c'],
        ['80', 'complete.c', 'complete.a'],

        # # a chain with a shared duplicate
        ['90', 'chain.a', 'chain.ab'],
        ['90', 'chain.ab', 'chain.b'],

        # a complex graph -- diamond
        ['60', 'cx1.WEST', 'cx1.NORTH'],
        ['70', 'cx1.WEST', 'cx1.SOUTH'],
        ['80', 'cx1.EAST', 'cx1.NORTH'],
        ['90', 'cx1.EAST', 'cx1.SOUTH'],

        # a complex graph -- two triangles with a shared point
        ['95', 'cx2.A1', 'cx2.A2'],
        ['95', 'cx2.A2', 'cx2.SHARE'],
        ['95', 'cx2.A1', 'cx2.SHARE'],
        ['95', 'cx2.B1', 'cx2.B2'],
        ['95', 'cx2.B2', 'cx2.SHARE'],
        ['95', 'cx2.B1', 'cx2.SHARE'],
        ]

class TestLinkFilter(unittest.TestCase):
    """Tests for LinkFilter"""

    def test_all(all):
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
    
        print('remove leaves:\n', ls.remove_leaves(), '\n', ls.links, '\n')

    def test_filter_nodes(self):
        ls = LinkFilter(test_links)
        print('filter nodes (components):\n',
              ls.filter_nodes(source='components'))
        print('filter nodes (components) - keep:\n',
              ls.filter_nodes(source='components', filter='keep'))
        print('filter nodes (components) - remove:\n',
              ls.filter_nodes(source='components', filter='remove'))

    def test_filter_nodes_scores(self):
        ls = LinkFilter(test_links_scores)
        print('filter nodes (components):\n',
              ls.filter_nodes(source='components'))


runner = unittest.TextTestRunner()
result = runner.run(unittest.makeSuite(TestLinkFilter))
print(result)
