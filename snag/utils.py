from collections import OrderedDict

import numpy as np
from netCDF4 import num2date
from xarray import DataArray
from cf_units import Unit

def merge_dicts(a, b):
    """
    Merge dicts a and b, with values in b overriding a

    Merges at the the second level. i.e. Merges dict top level values
    :return: New dict
    """
    c = a.copy()
    for k in b:
        if k not in c:
            c[k] = b[k]
        else:
            c[k].update(b[k])
    return c


def is_multi_time(time_idx):
    if isinstance(time_idx, slice) or time_idx is None:
        return True
    return False


def extract_times(nc_file, time_idx):
    multitime = is_multi_time(time_idx)

    dt = "datetime64[ns]"
    time_list = num2date(nc_file['time'][:], nc_file['time'].units)
    time_arr = np.asarray(time_list, dtype=dt)

    outattrs = OrderedDict()
    outcoords = None

    outdimnames = ["time"]
    outname = "times"
    outattrs["description"] = "times"

    outarr = DataArray(time_arr, name=outname, coords=outcoords,
                       dims=outdimnames, attrs=outattrs)

    if not multitime:
        return outarr[time_idx]

    return outarr


def extract_vars(nc_file, var_name, time_idx=None, target_units=None):
    """
    Return a :class:`xarray.DataArray` object for the desired variable in a single NetCDF file object.

    Adapted from wrf.util

    :param ncfile: (:class:`netCDF4.Dataset`, :class:`Nio.NioFile`): An open netCDF file
    :param var_name: (:obj:`str`) The variable name.
    :param time_idx: (:obj:`int` or :data:`wrf.ALL_TIMES`, optional): The desired time index. This value can be a positive integer, negative integer,
            or None to return all times in the file or sequence. The default is None (return all idxs).
    :param  target_units: (:obj:`str`) If not None, attempt to convert units to this format using cf_units.
    :returns: :class:`xarray.DataArray`:  An array object that contains metadata.

    """
    multitime = is_multi_time(time_idx)
    time_idx_or_slice = time_idx if not multitime else slice(None)
    var = nc_file.variables[var_name]
    if len(var.shape) > 1:
        data = var[time_idx_or_slice, :]
    else:
        data = var[time_idx_or_slice]

    if target_units is not None and hasattr(var, 'units'):
        u = Unit(var.units)
        data = u.convert(data, target_units)

    # Want to preserve the time dimension
    if not multitime:
        if len(var.shape) > 1:
            data = data[np.newaxis, :]
        else:
            data = data[np.newaxis]

    attrs = OrderedDict()
    for dkey, val in var.__dict__.items():
        # scipy.io adds these but don't want them
        if dkey in ("data", "_shape", "_size", "_typecode", "_attributes",
                    "maskandscale", "dimensions"):
            continue

        _dkey = dkey if isinstance(dkey, str) else dkey.decode()
        attrs[_dkey] = val

    dimnames = var.dimensions[-data.ndim:]

    coords = OrderedDict()

    if dimnames[0] == "time":
        t = extract_times(nc_file, time_idx)
        if not multitime:
            t = [t]
        coords[dimnames[0]] = t

    if len(dimnames) == 2 and dimnames[1] == 'height': #TODO: Make generic
        t = extract_vars(nc_file, 'height', slice(None), target_units='m')
        coords['height'] = t

    data_array = DataArray(data, name=nc_file, dims=dimnames, coords=coords, attrs=attrs)

    return data_array


def to_np(arr):
    """
    Converts a xarray.DataArray to a numpy.ndarray

    Adapted from wrf.util.to_np

    If the :class:`xarray.DataArray` instance does not contain a *_FillValue*
    or *missing_value* attribute, then this routine simply returns the
    :attr:`xarray.DataArray.values` attribute.  If the
    :class:`xarray.DataArray` object contains a *_FillValue* or *missing_value*
    attribute, then this routine returns a :class:`numpy.ma.MaskedArray`
    instance, where the NaN values (used by xarray to represent missing data)
    are replaced with the fill value.

    If the object passed in to this routine is not an
    :class:`xarray.DataArray` instance, then this routine simply returns the
    passed in object.  This is useful in situations where you do not know
    if you have an :class:`xarray.DataArray` or a :class:`numpy.ndarray` and
    simply want a :class:`numpy.ndarray` returned.

    :param arr: Can be any object type, but is generally used with :class:`xarray.DataArray` or :class:`numpy.ndarray`.
    :returns: :class:`numpy.ndarray` or :class:`numpy.ma.MaskedArray`: The extracted array or the *array* object if *array* is not a :class:
        `xarray.DataArray` object..
    """

    try:
        fill_value = arr.attrs["_FillValue"]
    except AttributeError:
        result = arr  # Not a DataArray
    except KeyError:
        result = arr.values  # Does not have missing values
    else:
        result = np.ma.masked_invalid(arr.values, copy=False)
        result.set_fill_value(fill_value)

    return result
