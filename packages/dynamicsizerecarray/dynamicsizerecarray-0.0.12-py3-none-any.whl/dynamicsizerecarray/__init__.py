from .version import __version__
import numpy as np
import copy


class DynamicSizeRecarray:
    """
    A dynamic, appendable implementation of numpy.recarray.
    """

    def __init__(self, recarray=None, dtype=None, shape=0):
        """
        Either provide an existing recarray 'recarray' or
        provide the 'dtype' to start with an empty recarray.

        Parameters
        ----------
        recarray : numpy.recarray, default=None
            The start of the dynamic recarray.
        dtype : list(tuple("key", "dtype_str")), default=None
            The dtype of the dynamic recarray.
        shape : int
            The initial size. (Same as in np.recarray)
        """
        self._size = 0
        if recarray is None and dtype == None:
            raise AttributeError("Requires either 'recarray' or 'dtype'.")
        if recarray is not None and dtype is not None:
            raise AttributeError(
                "Expected either one of 'recarray' or' dtype' to be 'None'"
            )

        _minimal_capacity = 2

        if dtype:
            if shape < 0:
                raise AttributeError("Expected shape >= 0.")
            initial_capacity = np.max([_minimal_capacity, shape])
            self._recarray = np.recarray(
                shape=initial_capacity,
                dtype=dtype,
            )
            self._size = shape
        else:
            initial_capacity = np.max([_minimal_capacity, len(recarray)])
            self._recarray = np.recarray(
                shape=initial_capacity,
                dtype=recarray.dtype,
            )
            self.append_recarray(recarray=recarray)

    @property
    def shape(self):
        """
        Returns the appended/set shape (in number of records) of internal
        recarray.
        This is the shape a recarray will have when calling to_recarray().

        Returns
        -------
        shape : tuple(self.__len__(), )
        """
        return (self.__len__(),)

    @property
    def dtype(self):
        return self._recarray.dtype

    def _capacity(self):
        """
        Returns the capacity (in number of records) of the allocated memeory.
        This is the length of the internal recarray.
        """
        return len(self._recarray)

    def to_recarray(self):
        """
        Exports to a numpy.recarray.
        """
        out = np.recarray(
            shape=self._size,
            dtype=self._recarray.dtype,
        )
        out = self._recarray[0 : self._size]
        return out

    def append_record(self, record):
        """
        Append one record to the dynamic racarray.
        The size of the dynamic recarray will increase by one.

        Parameters
        ----------
        record : dict
            The record to be appended must have all the keys of the dynamic
            recarray. Additional keys in the reocrd will be ignored.
        """
        self._grow_if_needed(additional_size=1)
        for key in self._recarray.dtype.names:
            self._recarray[self._size][key] = record[key]
        self._size += 1

    def append_records(self, records):
        """
        Append the records to the dynamic racarray.
        The size of the dynamic recarray will increase by len(records).

        Parameters
        ----------
        record : list of dicts
            A list of records. Every record must have the keys of the internal,
            dynamic recarray.
        """
        for record in records:
            self.append_record(record=record)

    def append_recarray(self, recarray):
        """
        Append a recarray to the dynamic racarray.
        The size of the dynamic recarray will increase by len(recarray).

        Parameters
        ----------
        recarray : numpy.recarray
            This will be appended to the internal, dynamic recarray.
        """
        self._grow_if_needed(additional_size=len(recarray))
        start = self._size
        stop = start + len(recarray)
        self._recarray[start:stop] = recarray
        self._size += len(recarray)

    def _grow_if_needed(self, additional_size):
        assert additional_size >= 0
        current_capacity = self._capacity()
        required_size = self._size + additional_size

        if required_size > current_capacity:
            swp = copy.deepcopy(self._recarray)
            next_capacity = np.max([current_capacity * 2, required_size])
            self._recarray = np.recarray(
                shape=next_capacity,
                dtype=swp.dtype,
            )
            start = 0
            stop = self._size
            self._recarray[start:stop] = swp[0 : self._size]
            del swp

    def __limit_idx_to_valid_bounds(self, i):
        if i < 0:
            return 0
        elif i >= self._size:
            return self._size
        else:
            return i

    def _limit_idx_to_valid_bounds(self, idx):
        if isinstance(idx, slice):
            sl = {"start": None, "stop": self._size, "step": None}
            if idx.start:
                sl["start"] = self.__limit_idx_to_valid_bounds(i=idx.start)
            if idx.stop:
                sl["stop"] = self.__limit_idx_to_valid_bounds(i=idx.stop)
            if idx.step:
                sl["step"] = idx.step
            return slice(sl["start"], sl["stop"], sl["step"])
        else:
            self.__raise_IndexError_if_out_of_bounds(idx=idx)
            return idx

    def __raise_IndexError_if_out_of_bounds(self, idx):
        iii = np.asarray(idx)
        mask = iii >= self._size
        if np.any(mask):
            bad_iii = iii[mask]
            raise IndexError(
                f"index {str(bad_iii):s} is out of bounds for size {self._size:d}."
            )

    def tobytes(self):
        return self.to_recarray().tobytes()

    def __getitem__(self, idx):
        if isinstance(idx, str):
            return self._getitem_by_column_key_str(key=idx)
        else:
            return self._getitem_by_row_idx_int(idx=idx)

    def __setitem__(self, idx, value):
        if isinstance(idx, str):
            self._setitem_by_column_key_str(key=idx, value=value)
        else:
            self._setitem_by_row_idx_int(idx=idx, value=value)

    def _getitem_by_column_key_str(self, key):
        return self._recarray[key][0 : self.__len__()]

    def _getitem_by_row_idx_int(self, idx):
        midx = self._limit_idx_to_valid_bounds(idx=idx)
        return self._recarray[midx]

    def _setitem_by_row_idx_int(self, idx, value):
        midx = self._limit_idx_to_valid_bounds(idx=idx)
        self._recarray[midx] = value

    def _setitem_by_column_key_str(self, key, value):
        self._recarray[key][0 : self.__len__()] = value

    def __len__(self):
        return self._size

    def shrink_to_fit(self):
        """
        Reduces the allocated memory to a minimum.
        """
        _minimal_capacity = 2
        if (
            self._size < self._recarray.shape[0]
            and self._size >= _minimal_capacity
        ):
            self._recarray = copy.deepcopy(self._recarray[0 : self._size])

    def __repr__(self):
        out = "{:s}(dtype={:s})".format(
            self.__class__.__name__, str(self._recarray.dtype.descr)
        )
        return out
