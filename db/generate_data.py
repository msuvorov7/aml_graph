import arango


test_nodes = [
    {'_key': 'A', 'block_status': 1},
    {'_key': 'B', 'block_status': 0},
    {'_key': 'C', 'block_status': 0},
    {'_key': 'D', 'block_status': 0},
    {'_key': 'E', 'block_status': 1},
    {'_key': 'F', 'block_status': 0},
    {'_key': 'G', 'block_status': 0},
]


test_edges = [
    {'_key': '1', '_from': 'nodes/A', '_to': 'nodes/B', 'amount': 50, 'dlk_cob_date': '2023-12-20'},

    {'_key': '2', '_from': 'nodes/A', '_to': 'nodes/C', 'amount': 100, 'dlk_cob_date': '2023-12-20'},
    {'_key': '3', '_from': 'nodes/A', '_to': 'nodes/C', 'amount': 50, 'dlk_cob_date': '2023-12-20'},
    {'_key': '4', '_from': 'nodes/A', '_to': 'nodes/C', 'amount': 20, 'dlk_cob_date': '2023-12-24'},

    {'_key': '5', '_from': 'nodes/B', '_to': 'nodes/A', 'amount': 30, 'dlk_cob_date': '2023-12-20'},
    {'_key': '6', '_from': 'nodes/B', '_to': 'nodes/A', 'amount': 30, 'dlk_cob_date': '2023-12-21'},

    {'_key': '7', '_from': 'nodes/C', '_to': 'nodes/A', 'amount': 10, 'dlk_cob_date': '2023-12-20'},
    {'_key': '8', '_from': 'nodes/C', '_to': 'nodes/A', 'amount': 10, 'dlk_cob_date': '2023-12-21'},

    {'_key': '9', '_from': 'nodes/B', '_to': 'nodes/D', 'amount': 20, 'dlk_cob_date': '2023-12-20'},
    {'_key': '10', '_from': 'nodes/B', '_to': 'nodes/D', 'amount': 10, 'dlk_cob_date': '2023-12-20'},

    {'_key': '11', '_from': 'nodes/D', '_to': 'nodes/B', 'amount': 40, 'dlk_cob_date': '2023-12-20'},

    {'_key': '12', '_from': 'nodes/C', '_to': 'nodes/E', 'amount': 70, 'dlk_cob_date': '2023-12-20'},

    {'_key': '13', '_from': 'nodes/E', '_to': 'nodes/D', 'amount': 50, 'dlk_cob_date': '2023-12-20'},
    {'_key': '14', '_from': 'nodes/E', '_to': 'nodes/F', 'amount': 20, 'dlk_cob_date': '2023-12-20'},

    {'_key': '15', '_from': 'nodes/F', '_to': 'nodes/G', 'amount': 10, 'dlk_cob_date': '2023-12-20'},
    {'_key': '16', '_from': 'nodes/F', '_to': 'nodes/G', 'amount': 10, 'dlk_cob_date': '2023-12-21'},

    {'_key': '17', '_from': 'nodes/G', '_to': 'nodes/E', 'amount': 100, 'dlk_cob_date': '2023-12-20'},
    {'_key': '18', '_from': 'nodes/G', '_to': 'nodes/E', 'amount': 100, 'dlk_cob_date': '2023-12-21'},
]


if __name__ == '__main__':
    client = arango.ArangoClient()
    db = client.db(name='_system', username='root', password='root')

    nodes_con = db.create_collection(name='nodes')
    edges_con = db.create_collection(name='edges', edge=True)

    # существует метод insert_many для работы с множеством записей, но нестабильно работает для больших объемов
    for node in test_nodes:
        nodes_con.insert(node)

    for edge in test_edges:
        edges_con.insert(edge)

    test_graph = db.create_graph(name='test_transactions')
    test_graph.create_edge_definition(
        edge_collection='edges',
        from_vertex_collections=['nodes'],
        to_vertex_collections=['nodes']
    )

    print('graph created')
