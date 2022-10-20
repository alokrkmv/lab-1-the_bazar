from create_bazar import generate_graph, create_bazar, get_longest_path, get_hop_count


# nameserver
# create bazar is connected
# create bazaar graph getting created
# checks minimum number of buyrs and sellers

# d = [
# [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
# [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
# [0, 1, 0, 1, 0, 0, 0, 0, 0, 0],
# [0, 0, 1, 0, 1, 1, 0, 0, 0, 0],
# [0, 0, 0, 1, 0, 1, 1, 0, 0, 0],
# [0, 0, 0 ,0 ,1, 0, 1, 1, 0, 0],
# [0, 0, 0 ,0 ,1, 1, 0, 1, 0, 0],
# [0, 0, 0 ,0, 0, 1, 1, 0, 1, 0],
# [0, 0, 0 ,0, 0, 0, 0, 1, 0, 1],
# [0, 0, 0 ,0, 0, 0, 0, 0, 1, 0],
# ]

# d = [
#     [0, 1, 0, 0, 0, 1],
#     [1, 0, 1, 0, 0, 0],
#     [0, 1, 0, 1, 1, 0],
#     [0, 0, 1, 0, 1, 0],
#     [0, 0, 1, 1, 0, 1],
#     [1, 0, 0, 0, 1, 0]
# ]

def test_get_longest_path(self):
    d = [
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1],
        [1, 0, 0, 1, 0],
    ]
    print(get_longest_path(d))



