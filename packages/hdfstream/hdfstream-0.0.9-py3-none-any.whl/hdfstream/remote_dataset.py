#!/bin/env python

import numpy as np
import collections.abc


class RemoteDataset:
    """
    Object representing a HDF5 dataset in the remote file

    Parameters:

    connection: Connection object to use to send requests
    file_path: path to the file containing the HDF5 dataset
    name: name of the HDF5 dataset to open
    data: msgpack encoded dataset description
    """
    def __init__(self, connection, file_path, name, data, parent):

        self.connection = connection
        self.file_path = file_path
        self.name = name
        self.attrs = data["attributes"]
        self.dtype = np.dtype(data["type"])
        self.kind  = data["kind"]
        self.shape = tuple(data["shape"])
        self.ndim = len(self.shape)
        self.chunks = None
        if "data" in data:
            self.data = data["data"]
        else:
            self.data = None
        self.parent = parent

        # Compute total number of elements in the dataset
        size = 1
        for s in self.shape:
            size *= s
        self.size = size

        # Will return zero dimensional attributes as numpy scalars
        for name, arr in self.attrs.items():
            if hasattr(arr, "shape") and len(arr.shape) == 0:
                self.attrs[name] = arr[()]

    def _single_slice(self, start, count):
        """
        Fetch a slice of this dataset. May return fewer elements
        than requested if result is too large for a msgpack bin
        object.

        start: array of starting offsets in each dimension
        count: number of elements to fetch in each dimension
        """
        return self.connection.request_slice(self.file_path, self.name, start, count)

    def slice(self, start, count):
        """
        Repeatedly slice dataset until all requested elements
        have been received.
        """
        current_start = np.asarray(start, dtype=int).copy()
        current_count = np.asarray(count, dtype=int).copy()

        data = []
        while True:
            data.append(self._single_slice(current_start, current_count))
            if len(current_count) > 0:
                nr_read = data[-1].shape[0]
                current_count[0] -= nr_read
                current_start[0] += nr_read
                if current_count[0] == 0:
                    break
        return np.concatenate(data, axis=0)

    def __getitem__(self, key):
        """
        Fetch a dataset slice by indexing this object.

        Translates a numpy style tuple of integer/slice/ellipsis objects into
        the start and count parameters needed for the web API.
        """

        # Ensure key is at least a one element sequence
        if not isinstance(key, collections.abc.Sequence):
            key = (key,)

        start = []
        count = []
        dim_nr = 0
        found_ellipsis = False
        result_dim = []
        for k in key:
            if isinstance(k, int):
                # This is a single integer index
                start.append(k)
                count.append(1)
                dim_nr += 1
            elif isinstance(k, slice):
                # This is a slice. Step must be one, if specified.
                if k.step != 1 and k.step != None:
                    raise KeyError("RemoteDataset slices with step != 1 are not supported")
                # Find start and stop parameters
                slice_start = k.start if k.start is not None else 0
                slice_stop = k.stop if k.stop is not None else self.shape[dim_nr]
                start.append(slice_start)
                count.append(slice_stop-slice_start)
                dim_nr += 1
                result_dim.append(count[-1])
            elif k is Ellipsis:
                # This is an Ellipsis. Selects all elements in as many dimensions as needed.
                if found_ellipsis:
                    raise KeyError("RemoteDataset slices can only contain one Ellipsis")
                ellipsis_size = len(self.shape) - len(key) + 1
                if ellipsis_size < 0:
                    raise KeyError("RemoteDataset slice has more dimensions that the dataset")
                for i in range(ellipsis_size):
                    start.append(0)
                    count.append(self.shape[dim_nr])
                    dim_nr += 1
                    result_dim.append(count[-1])
                found_ellipsis = True
            else:
                raise KeyError("RemoteDataset index must be integer or slice")

        # If too few slices were specified, read all elements in the remaining dimensions
        for i in range(dim_nr, len(self.shape)):
            start.append(0)
            count.append(self.shape[i])

        if self.data is None:
            # Dataset is not in memory, so request it from the server
            data = self.slice(start, count)
            # Remove any dimensions where the index was a scalar, for
            # consistency with numpy
            data = data.reshape(result_dim)
            # In case of scalar results, don't wrap in a numpy scalar
            if isinstance(data, np.ndarray):
                if len(data.shape) == 0:
                    return data[()]
            return data
        else:
            # Dataset was already loaded with the metadata
            return self.data[key]

    def __repr__(self):
        return f'<Remote HDF5 dataset "{self.name}" shape {self.shape}, type "{self.dtype.str}">'

    def read_direct(self, array, source_sel=None, dest_sel=None):
        """
        Mimic h5py's Dataset.read_direct() method.

        For compatibility only. There's no performance benefit here.
        """
        if source_sel is None:
            source_sel = Ellipsis
        if dest_sel is None:
            dest_sel = Ellipsis
        array[dest_sel] = self[source_sel]

    def __len__(self):
        if len(self.shape) >= 1:
            return self.shape[0]
        else:
            raise TypeError("len() is not supported for scalar datasets")

    def close(self):
        """
        There's nothing to close, but some code might expect this to exist
        """
        pass
