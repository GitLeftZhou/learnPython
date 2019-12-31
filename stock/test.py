from pandas import PeriodIndex, DatetimeIndex, Int64Index, RangeIndex


def _get_index_loc(self, key, base_index=None):

   if base_index is None:
        base_index = self._index

    index = base_index
    date_index = isinstance(base_index, (PeriodIndex, DatetimeIndex))
    int_index = isinstance(base_index, Int64Index)
    range_index = isinstance(base_index, RangeIndex)
    index_class = type(base_index)
    nobs = len(index)

    # Special handling for RangeIndex
    if range_index and isinstance(key, (int, long, np.integer)):
        # Negative indices (that lie in the Index)
        if key < 0 and -key <= nobs:
            key = nobs + key
        # Out-of-sample (note that we include key itself in the new index)
        elif key > nobs - 1:
            # See gh5835. Remove the except after pandas 0.25 required.
            try:
                base_index_start = base_index.start
                base_index_step = base_index.step
            except AttributeError:
                base_index_start = base_index._start
                base_index_step = base_index._step
            stop = base_index_start + (key + 1) * base_index_step
            index = RangeIndex(start=base_index_start,
                               stop=stop,
                               step=base_index_step)

    # Special handling for Int64Index
    if (not range_index and int_index and not date_index and
            isinstance(key, (int, long, np.integer))):
        # Negative indices (that lie in the Index)
        if key < 0 and -key <= nobs:
            key = nobs + key
        # Out-of-sample (note that we include key itself in the new index)
        elif key > base_index[-1]:
            index = Int64Index(np.arange(base_index[0], int(key + 1)))

    # Special handling for date indexes
    if date_index:
        # Use index type to choose creation function
        if index_class is DatetimeIndex:
            index_fn = date_range
        else:
            index_fn = period_range
        # Integer key (i.e. already given a location)
        if isinstance(key, (int, long, np.integer)):
            # Negative indices (that lie in the Index)
            if key < 0 and -key < nobs:
                key = index[nobs + key]
            # Out-of-sample (note that we include key itself in the new
            # index)
            elif key > len(base_index) - 1:
                index = index_fn(start=base_index[0],
                                 periods=int(key + 1),
                                 freq=base_index.freq)
                key = index[-1]
            else:
                key = index[key]
        # Other key types (i.e. string date or some datetime-like object)
        else:
            # Covert the key to the appropriate date-like object
            if index_class is PeriodIndex:
                date_key = Period(key, freq=base_index.freq)
            else:
                date_key = Timestamp(key)

            # Out-of-sample
            if date_key > base_index[-1]:
                # First create an index that may not always include `key`
                index = index_fn(start=base_index[0], end=date_key,
                                 freq=base_index.freq)

                # Now make sure we include `key`
                if not index[-1] == date_key:
                    index = index_fn(start=base_index[0],
                                     periods=len(index) + 1,
                                     freq=base_index.freq)

    # Get the location
    if date_index:
        # (note that get_loc will throw a KeyError if key is invalid)
        loc = index.get_loc(key)
    elif int_index or range_index:
        # For Int64Index and RangeIndex, key is assumed to be the location
        # and not an index value (this assumption is required to support
        # RangeIndex)
        try:
            index[key]
        # We want to raise a KeyError in this case, to keep the exception
        # consistent across index types.
        # - Attempting to index with an out-of-bound location (e.g.
        #   index[10] on an index of length 9) will raise an IndexError
        #   (as of Pandas 0.22)
        # - Attemtping to index with a type that cannot be cast to integer
        #   (e.g. a non-numeric string) will raise a ValueError if the
        #   index is RangeIndex (otherwise will raise an IndexError)
        #   (as of Pandas 0.22)
        except (IndexError, ValueError) as e:
            raise KeyError(str(e))
        loc = key
    else:
        loc = index.get_loc(key)

    # Check if we now have a modified index
    index_was_expanded = index is not base_index

    # Return the index through the end of the loc / slice
    if isinstance(loc, slice):
        end = loc.stop
    else:
        end = loc

    return loc, index[:end + 1], index_was_expanded