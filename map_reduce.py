import collections
import multiprocessing
import itertools


class MapReduce(object):
    def __init__(self, map_function, reduce_function, no_workers=None):
        self.map_function = map_function
        self.reduce_function = reduce_function
        self.pool = multiprocessing.Pool(no_workers)

    @staticmethod
    def shuffle_and_sort(mapped_values):
        partitioned_data = collections.defaultdict(list)
        for key, value in mapped_values:
            partitioned_data[key].append(value)
        return partitioned_data.items()

    def __call__(self, inputs, chunksize=1):
        map_responses = self.pool.map(self.map_function, inputs, chunksize)
        partitioned_data = []
        for response in map_responses:
            partitioned_data.append(self.shuffle_and_sort(itertools.chain(*response[0])))
        reduced_values = self.pool.map(self.reduce_function, partitioned_data)
        return reduced_values
