import abc
from typing import Any, Callable, Mapping, Union

import numpy as np
import unyt
import xarray as xr
import yt
from numpy import typing as npt
from unyt import earth_radius as _earth_radius

from yt_xarray.accessor import _xr_to_yt
from yt_xarray.utilities.logging import ytxr_log

EARTH_RADIUS = _earth_radius * 1.0


class Transformer(abc.ABC):
    """
    The transformer base class, meant to be subclassed, do not instantiate directly.

    Parameters
    ----------
    native_coords: tuple[str, ...]
        the names of the native coordinates, e.g., ('x0', 'y0', 'z0'), on
        which data is defined.
    transformed_coords: tuple[str, ...]
        the names of the transformed coordinates, e.g., ('x1', 'y1', 'z1')
    coord_aliases: dict
        optional dictionary of coordinate aliases to map arbitrary keys to
        a native or transformed coordinate name.

    the names of the coordinates will be expected as keyword arguments in the
    'to_native' and 'to_transformed' methods.

    """

    def __init__(
        self,
        native_coords: tuple[str, ...],
        transformed_coords: tuple[str, ...],
        coord_aliases: dict[str, str] | None = None,
    ):
        self.native_coords = native_coords
        self._native_coords_set = set(native_coords)
        self.transformed_coords = transformed_coords
        self._transformed_coords_set = set(transformed_coords)

        self._native_coord_index = {
            native_coords[i]: i for i in range(len(native_coords))
        }
        self._transformed_coord_index = {
            transformed_coords[i]: i for i in range(len(transformed_coords))
        }

        if coord_aliases is None:
            coord_aliases = {}

        for ky, val in coord_aliases.items():
            if (
                val not in self._native_coords_set
                and val not in self._transformed_coords_set
            ):
                msg = (
                    f"Coordinate alias {ky} must point to a valid native or transformed "
                    f"coordinate name: {self._native_coords_set}, {self._transformed_coords_set}"
                    f" but {ky}={val}."
                )
                raise ValueError(msg)
        self.coord_aliases = coord_aliases

    def _disambiguate_coord(self, coord: str) -> str:
        if coord in self.native_coords or coord in self.transformed_coords:
            return coord

        if coord in self.coord_aliases:
            return self.coord_aliases[coord]

        msg = f"Coordinate name {coord} not found in valid coordinates or in coordinate aliases."
        raise ValueError(msg)

    @abc.abstractmethod
    def _calculate_native(self, **coords) -> list[npt.NDArray]:
        """
        function to convert from transformed to native coordinates. Must be
        implemented by each child class.
        """

    @abc.abstractmethod
    def _calculate_transformed(self, **coords) -> list[npt.NDArray]:
        """
        function to convert from native to transformed coordinates. Must be
        implemented by each child class.
        """

    def _validate_input_coords(self, coords, input_coord_type: str):
        assert input_coord_type in ("native", "transformed")

        valid_coords_names = getattr(self, f"{input_coord_type}_coords")
        valid_coords_set = getattr(self, f"_{input_coord_type}_coords_set")

        new_coords = {}

        dim_set = set()
        for dim0 in coords.keys():
            # check for validity of each dim
            dim = self._disambiguate_coord(dim0)
            new_coords[dim] = coords[dim0]
            dim_set.add(dim)

        # check that all required coordinates are present
        if dim_set != valid_coords_set:
            # find the missing one and raise an error
            for dim in valid_coords_names:
                if dim not in coords:
                    msg = (
                        f"The {input_coord_type} coordinate {dim} was not specified."
                        " Please provide it as an additional keyword argument."
                    )
                    raise RuntimeError(msg)

        return new_coords

    def to_native(self, **coords: npt.NDArray) -> list[npt.NDArray]:
        """
        Calculate the native coordinates from transformed coordinates.

        Parameters
        ----------
        coords:
            coordinate values in transformed coordinate system, provided as
            individual keyword arguments.

        Returns
        -------
        list
            coordinate values in the native coordinate system, in order
            of the native_coords attribute.

        """

        # Generally, no need to override this interp_method, the actual
        # coordinate transformation implementation should happen by
        # overriding `_calculate_native`

        new_coords = self._validate_input_coords(coords, "transformed")
        return self._calculate_native(**new_coords)

    def to_transformed(self, **coords: npt.NDArray) -> list[npt.NDArray]:
        """
        Calculate the transformed coordinates from native coordinates.

        Parameters
        ----------
        coords:
            coordinate values in native coordinate system, provided as
            individual keyword arguments.

        Returns
        -------
        list
            coordinate values in the transformed coordinate system, in order
            of the transformed_coords attribute.

        """

        # Generally, no need to override this interp_method, the actual
        # coordinate transformation implementation should happen by
        # overriding `_calculate_transformed`
        new_coords = self._validate_input_coords(coords, "native")
        return self._calculate_transformed(**new_coords)

    @abc.abstractmethod
    def calculate_transformed_bbox(
        self, bbox_dict: Mapping[str, npt.NDArray]
    ) -> npt.NDArray:
        """
        Calculates a bounding box in transformed coordinates for a bounding box dictionary
        in native coordinates.

        Parameters
        ----------
        bbox_dict : dict
            dictionary with the ranges for each native dimension.

        Returns
        -------
        np.ndarray
            2D bounding box array
        """


class LinearScale(Transformer):
    """
    A transformer that linearly scales between coordinate systems.

    This transformer is mostly useful for demonstration purposes and simply
    applies a constant scaling factor for each dimension:

        (x_sc, y_sc, z_sc) = (x_scale, y_scale, z_scale) * (x, y, z)

    Parameters
    ----------
    native_coords: tuple[str, ...]
        the names of the native coordinates, e.g., ('x', 'y', 'z'), on
        which data is defined.
    scale: dict
        a dictionary containing the scale factor for each dimension. keys
        should match the native_coords names and missing keys default to a
        value of 1.0

    The scaled coordinate names are given by appending `'_sc'` to each native
    coordinate name. e.g., if `native_coords=('x', 'y', 'z')`, then the
    transformed coordinate names are ('x_sc', 'y_sc', 'z_sc').

    Examples
    --------

    >>> from yt_xarray.transformations import LinearScale
    >>> native_coords = ('x', 'y', 'z')
    >>> scale_factors = {'x': 2., 'y':3., 'z':1.5}
    >>> lin_scale = LinearScale(native_coords, scale_factors)
    >>> print(lin_scale.to_transformed(x=1, y=1, z=1))
    [2., 3., 1.5]
    >>> print(lin_scale.to_native(x_sc=2., y_sc=3., z_sc=1.5))
    [1., 1., 1.]

    """

    def __init__(
        self, native_coords: tuple[str, ...], scale: dict[str, float] | None = None
    ):
        if scale is None:
            scale = {}

        for nc in native_coords:
            if nc not in scale:
                scale[nc] = 1.0
        self.scale = scale
        transformed_coords = tuple([nc + "_sc" for nc in native_coords])
        super().__init__(native_coords, transformed_coords)

    def _calculate_transformed(self, **coords) -> list[npt.NDArray]:
        transformed = []
        for nc_sc in self.transformed_coords:
            nc = nc_sc[:-3]  # native coord name. e.g., go from "x_sc" to just "x"
            transformed.append(np.asarray(coords[nc]) * self.scale[nc])
        return transformed

    def _calculate_native(self, **coords) -> list[npt.NDArray]:
        native = []
        for nc in self.native_coords:
            native.append(np.asarray(coords[nc + "_sc"]) / self.scale[nc])
        return native

    def calculate_transformed_bbox(
        self, bbox_dict: Mapping[str, npt.NDArray]
    ) -> npt.NDArray:
        """
        Calculates a bounding box in transformed coordinates for a bounding box dictionary
        in native coordinates.

        Parameters
        ----------
        bbox_dict : dict
            dictionary with the ranges for each native dimension.

        Returns
        -------
        np.ndarray
            2D bounding box array
        """

        # since this is a linear scaling, bbox dims will be independent and
        # can simply treat the bounding box as the points
        transformed = self.to_transformed(**bbox_dict)
        return transformed


_default_radial_axes = dict(
    zip(("radius", "depth", "altitude"), ("radius", "depth", "altitude"))
)


def _sphere_to_cart(
    r: npt.NDArray, theta: npt.NDArray, phi: npt.NDArray
) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray]:
    # r : radius
    # theta: colatitude
    # phi: azimuth
    # returns x, y, z
    z = r * np.cos(theta)
    xy = r * np.sin(theta)
    x = xy * np.cos(phi)
    y = xy * np.sin(phi)
    return x, y, z


def _cart_to_sphere(
    x: npt.NDArray, y: npt.NDArray, z: npt.NDArray
) -> tuple[npt.NDArray, npt.NDArray, npt.NDArray]:
    # will return phi (azimuth) in +/- np.pi
    r = np.sqrt(x * x + y * y + z * z)
    theta = np.arccos(z / (r + 1e-12))
    phi = np.arctan2(y, x)
    return r, theta, phi


class GeocentricCartesian(Transformer):
    """
    A transformer to convert between Geodetic coordinates and cartesian,
    geocentric coordinates.

    Parameters
    ----------
    radial_type: str
        one of ("radius", "depth", "altitude") to indicate the type of
        radial axis.
    radial_axis: str
        Optional string to use as the name for the radial axis, defaults to
        whatever you provide for radial_type.
    r_o: float like
        The reference radius, default is the radius of the Earth.
    coord_aliases: dict
        Optional dictionary of additional coordinate aliases.
    use_neg_lons: bool
        If False (the default), will expect longitude in the range 0, 360. If
        True, will expect longitude in the range -180, 180.

    transformed_coords names are ("x", "y", "z") and
    native_coords names are (radial_axis, "latitude", "longitude"). Supply
    latitude and longitude vlaues in degrees.

    Examples
    --------

    >>> from yt_xarray.transformations import GeocentricCartesian
    >>> gc = GeocentricCartesian("depth")
    >>> x, y, z = gc.to_transformed(depth=100., latitude=42., longitude=220.)
    >>> print((x, y, z))
    # (-3626843.0297669284, -3043282.6486153184, 4262969.546178633)
    >>> print(gc.to_native(x=x,y=y,z=z))
    # (100.00000000093132, 42.0, 220.0)

    """

    def __init__(
        self,
        radial_type: str = "radius",
        radial_axis: str | None = None,
        r_o: Union[float, unyt.unyt_quantity] | None = None,
        coord_aliases: dict[str, str] | None = None,
        use_neg_lons: bool = False,
    ):
        transformed_coords = ("x", "y", "z")

        valid_radial_types = ("radius", "depth", "altitude")
        if radial_type not in valid_radial_types:
            msg = (
                f"radial_type must be one of {valid_radial_types}, "
                f"found {radial_type}."
            )
            raise ValueError(msg)
        self.radial_type = radial_type

        if r_o is None:
            r_o = EARTH_RADIUS.to("m").d
        self._r_o = r_o

        if radial_axis is None:
            radial_axis = _default_radial_axes[radial_type]
        self.radial_axis = radial_axis
        native_coords = (radial_axis, "latitude", "longitude")
        self.use_neg_lons = use_neg_lons

        super().__init__(native_coords, transformed_coords, coord_aliases=coord_aliases)

    def _calculate_transformed(self, **coords) -> list[npt.NDArray]:
        if self.radial_type == "depth":
            r_val = self._r_o - coords[self.radial_axis]
        elif self.radial_type == "altitude":
            r_val = self._r_o + coords[self.radial_axis]
        else:
            r_val = coords[self.radial_axis]

        lat, lon = coords["latitude"], coords["longitude"]
        theta = (90.0 - lat) * np.pi / 180.0  # colatitude in radians
        phi = lon * np.pi / 180.0  # azimuth in radians
        x, y, z = _sphere_to_cart(r_val, theta, phi)
        return [x, y, z]

    def _calculate_native(self, **coords) -> list[npt.NDArray]:
        r, theta, phi = _cart_to_sphere(coords["x"], coords["y"], coords["z"])
        lat = 90.0 - theta * 180.0 / np.pi
        lon = phi * 180.0 / np.pi
        if self.use_neg_lons is False:
            if isinstance(lon, float):
                if lon < 0:
                    lon = lon + 360.0
            else:
                lon = np.mod(lon, 360.0)
        if self.radial_type == "altitude":
            r = r - self._r_o
        elif self.radial_type == "depth":
            r = self._r_o - r
        return [r, lat, lon]

    def calculate_transformed_bbox(
        self, bbox_dict: Mapping[str, npt.NDArray]
    ) -> npt.NDArray:
        """
        Calculates a bounding box in transformed coordinates for a bounding box dictionary
        in native coordinates.

        Parameters
        ----------
        bbox_dict : dict
            dictionary with the ranges for each native dimension.

        Returns
        -------
        np.ndarray
            2D bounding box array
        """

        bbox_valid = {}
        for ky in bbox_dict.keys():
            coord = self._disambiguate_coord(ky)
            bbox_valid[coord] = bbox_dict[ky]

        la = "latitude"
        lo = "longitude"
        test_lons = np.linspace(bbox_valid[lo][0], bbox_valid[lo][1], 200)
        test_lats = np.linspace(bbox_valid[la][0], bbox_valid[la][1], 200)

        test_lats, test_lons = np.meshgrid(test_lats, test_lons)
        test_lats = np.ravel(test_lats)
        test_lons = np.ravel(test_lons)

        rmin = bbox_valid[self.radial_axis][0]
        cs_to_transform = {self.radial_axis: rmin, la: test_lats, lo: test_lons}
        x_y_z = self.to_transformed(**cs_to_transform)
        bbox_cart = []
        for idim in range(3):
            bbox_cart.append([np.min(x_y_z[idim]), np.max(x_y_z[idim])])

        rmax = bbox_dict[self.radial_axis][1]
        cs_to_transform = {self.radial_axis: rmax, la: test_lats, lo: test_lons}
        x_y_z = self.to_transformed(**cs_to_transform)
        for idim in range(3):
            bbox_cart[idim][0] = np.min((np.min(x_y_z[idim]), bbox_cart[idim][0]))
            bbox_cart[idim][1] = np.max((np.max(x_y_z[idim]), bbox_cart[idim][1]))
        bbox_cart = np.array(bbox_cart)

        return bbox_cart


def build_interpolated_cartesian_ds(
    xr_ds: xr.Dataset,
    transformer: Transformer,
    fields: Union[str, tuple[str, ...], list[str]] | None = None,
    grid_resolution: tuple[int, ...] | list[int] | None = None,
    fill_value: float | None = None,
    length_unit: str | float = "km",
    refine_grid: bool = False,
    refine_by: int = 2,
    refine_max_iters: int = 200,
    refine_min_grid_size: int = 10,
    refinement_method: str = "division",
    sel_dict: dict[str, Any] | None = None,
    sel_dict_type: str = "isel",
    bbox_dict: Mapping[str, npt.NDArray] | None = None,
    interp_method: str = "nearest",
    interp_func: Callable[..., npt.NDArray] | None = None,
):
    """
    Build a yt cartesian dataset containing fields interpolated on demand
    from data defined on a 3D Geodetic grid to a uniform, cartesian grid

    Parameters
    ----------
    xr_ds: xr.Dataset
        the xarray dataset
    transformer:
        a Transformer instance that will convert between 3D cartesian coordinates
        and the native coordinates of the dataset
    fields: tuple
        the fields to include
    grid_resolution:
        the interpolated grid resolution, defaults to (64, 64, 64)
    fill_value: float
        Optional value to use for filling grid values that fall outside
        the original data. Defaults to np.nan, but for volume rendering
        you may want to adjust this.
    length_unit: str
        the length unit to use, defaults to 'km'
    refine_grid: bool
        if True (default False), will decompose the interpolated grid one level.
    refine_max_iters: int
        if refine_grid is True, max iterations for grid refinement (default 200)
    refine_min_grid_size:
        if refine_grid is True, minimum number of elements in refined grid (default 10)
    refinement_method:
        One of ``'division'`` (the default) or ``'signature_filter'``. If ``'division'``,
        refinement will proceed by iterative bisection in each dimension. If
        ``'signature_filter'``, will use the image mask signature decomposition
        of Berger and Rigoutsos 1991 (https://doi.org/10.1109/21.120081).
    interp_method: str
        interpolation method: ``'nearest'`` or ``'interpolate'``. Defaults to ``'nearest'``.
        If ``'interpolate'``, will use linear nd interpolation.
    interp_func: Callable
        a custom interpolation function. Will over-ride `interp_method`. The function
        will be called with ``interp_func(data=data_array, coords=eval_coords)``, where
        ``data_array`` is an xarray ``DataArray`` and ``eval_coords`` is a list of 1d
        np.ndarray ordered by the transformer native coordinate order and should
        return an np.ndarray of the same shape as the ``eval_coords``


    Returns
    -------
    yt.Dataset
        a yt dataset: cartesian, uniform grid with references to the
        provided xarray dataset. Interpolation from geodetic to geocentric
        cartesian happens on demand on data reads.

    """

    valid_methods = ("interpolate", "nearest")
    if interp_method not in valid_methods:
        msg = f"interp_method must be one of: {valid_methods}, found {interp_method}."
        raise ValueError(msg)
    if interp_func is not None:
        if interp_method == "nearest":
            ytxr_log.info(
                "Interpolation function provided, switching interp_method to 'interpolate'."
            )
            interp_method = "interpolate"

    valid_fields: list[str]
    if fields is None:
        valid_fields = list(xr_ds.data_vars)
    elif isinstance(fields, str):
        valid_fields = [
            fields,
        ]
    else:
        valid_fields = [f for f in fields]

    sel_info = _xr_to_yt.Selection(
        xr_ds,
        fields=valid_fields,
        sel_dict=sel_dict,
        sel_dict_type=sel_dict_type,
    )

    if bbox_dict is None:
        bbox_dict = {}  # the bbox in native coordinates, as a dictionary
        for ic, c in enumerate(sel_info.selected_coords):
            bbox_dict[c] = sel_info.selected_bbox[ic, :]

    if fill_value is None:
        fill_value = np.nan

    # calculate the cartesian bounding box
    bbox_cart = transformer.calculate_transformed_bbox(bbox_dict)
    bbox_native_valid = {}  # native coord bbox dict, with validated names as keys
    for ky in bbox_dict.keys():
        coord = transformer._disambiguate_coord(ky)
        bbox_native_valid[coord] = bbox_dict[ky]

    # round ? make this an option...
    bbox_cart[:, 0] = np.floor(bbox_cart[:, 0])
    bbox_cart[:, 1] = np.ceil(bbox_cart[:, 1])

    def _read_data(grid, field_name):
        xyz = grid.fcoords.to("code_length").d
        x = xyz[:, 0]
        y = xyz[:, 1]
        z = xyz[:, 2]

        mask, native_coords = _build_interpolated_domain_mask(
            x, y, z, transformer, bbox_native_valid
        )

        # interpolate
        output_vals = np.full(mask.shape, fill_value, dtype="float64")
        if np.any(mask):
            data = xr_ds.data_vars[field_name[1]]

            # first apply initial selection
            if len(sel_info.sel_dict) > 0:
                if sel_info.sel_dict_type == "sel":
                    data = data.sel(sel_info.sel_dict)
                else:
                    data = data.isel(sel_info.sel_dict)

            if interp_func is not None:
                native_coords_1 = [
                    native_coords[idim].ravel()[mask] for idim in range(3)
                ]
                vals = interp_func(data=data, coords=native_coords_1)
                output_vals[mask] = vals
            else:
                # now interpolate
                interp_dict = {}
                for dim in sel_info.selected_coords:
                    known_dim = transformer._disambiguate_coord(dim)
                    idim = transformer._native_coord_index[known_dim]
                    interp_dict[dim] = xr.DataArray(
                        native_coords[idim].ravel()[mask], dims="points"
                    )
                if interp_method == "interpolate":
                    vals = data.interp(
                        kwargs=dict(fill_value=fill_value), **interp_dict
                    )
                elif interp_method == "nearest":
                    vals = data.sel(interp_dict, method="nearest")

                output_vals[mask] = vals.to_numpy()

        output_vals = np.reshape(output_vals, grid.shape)

        return output_vals

    data_dict: dict[str, Callable[..., npt.NDArray]] = {}
    for field in valid_fields:
        data_dict[field] = _read_data

    if grid_resolution is None:
        grid_resolution = (64, 64, 64)

    if refine_grid:
        from yt_xarray.utilities._grid_decomposition import (
            _create_image_mask,
            _get_yt_ds,
        )

        # create an image mask within bbox
        ytxr_log.info("Creating image mask for grid decomposition.")

        bbox_geo = []
        for ax in transformer.native_coords:
            bbox_geo.append(bbox_native_valid[ax])
        bbox_geo = np.array(bbox_geo)
        image_mask = _create_image_mask(
            bbox_cart, bbox_geo, grid_resolution, transformer, chunks=50
        )
        ytxr_log.info("Decomposing image mask and building yt dataset.")

        return _get_yt_ds(
            image_mask,
            data_dict,
            bbox_cart,
            max_iters=refine_max_iters,
            min_grid_size=refine_min_grid_size,
            refine_by=refine_by,
            length_unit=length_unit,
            refinement_method=refinement_method,
        )

    ds = yt.load_uniform_grid(
        data_dict,
        grid_resolution,
        geometry="cartesian",
        bbox=bbox_cart,
        length_unit=length_unit,
        axis_order="xyz",
        nprocs=1,  # placeholder, should relax this when possible.
    )

    return ds


def _build_interpolated_domain_mask(x, y, z, transformer: Transformer, bbox_native):
    native_coords = transformer.to_native(x=x, y=y, z=z)

    mask = np.full(native_coords[0].shape, True, dtype=bool)
    for icoord in range(3):
        cname = transformer.native_coords[icoord]
        dim_range = bbox_native[cname]
        coord = native_coords[icoord]
        c_mask = np.logical_and(coord >= dim_range[0], coord <= dim_range[1])
        mask = np.logical_and(mask, c_mask)

    return mask, native_coords
