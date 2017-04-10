
import ipywidgets as widgets

from traitlets import Float, Bool, Unicode, CUnicode, List, observe, validate

from . import geotraitlets
from .locations import locations_to_latlng


class Polyline(widgets.Widget):
    """
    Polyline layer.

    Add this to a ``Map`` instance to draw a poly line.

    Data is a list of latitude, longitude tuples.

    :Examples:

    >>> m = gmaps.Map()
    >>> data = [(48.85341, 2.3488), (50.85045, 4.34878), (52.37403, 4.88969)]
    >>> polyline_layer = gmaps.Polyline(data=data)
    >>> m.add_layer(polyline_layer)

    :param data: List of (latitude, longitude) pairs denoting a single
        point. The first pair denotes the starting point and the last pair
        denote the end of the polyline.
        Latitudes are expressed as a float between -90
        (corresponding to 90 degrees south) and +90 (corresponding to
        90 degrees north). Longitudes are expressed as a float
        between -180 (corresponding to 180 degrees west) and 180
        (corresponding to 180 degrees east).
    :type data: list of tuples of length >= 2
    """
    has_bounds = True
    _view_name = Unicode("PolylineLayerView").tag(sync=True)
    _view_module = Unicode("jupyter-gmaps").tag(sync=True)
    _model_name = Unicode("PolylineLayerModel").tag(sync=True)
    _model_module = Unicode("jupyter-gmaps").tag(sync=True)

    geodesic = Bool(default_value=True).tag(sync=True)
    stroke_color = geotraitlets.ColorAlpha(
        default_value="#FF0000"
    ).tag(sync=True)
    stroke_opacity = Float(default_value=1.0, min=0.0, max=1.0).tag(sync=True)
    stroke_weight = Float(default_value=2, min=1.0, max=5.0).tag(sync=True)

    data = List(minlen=2).tag(sync=True)
    data_bounds = List().tag(sync=True)

    @validate("data")
    def _validate_data(self, proposal):
        for point in proposal["value"]:
            if not geotraitlets.is_valid_point((point['lat'],point['lng'])):
                raise geotraitlets.InvalidPointException(
                    "{} is not a valid latitude, longitude pair".format(point))
        return proposal["value"]

    @observe("data")
    def _calc_bounds(self, change):
        data = change["new"]
        min_latitude = min(row['lat'] for row in data)
        min_longitude = min(row['lng'] for row in data)
        max_latitude = max(row['lat'] for row in data)
        max_longitude = max(row['lng'] for row in data)
        self.data_bounds = [
            (min_latitude, min_longitude),
            (max_latitude, max_longitude)
        ]


def _polyline_options(points, geodesic, stroke_color, stroke_opacity, stroke_weight):
    data = locations_to_latlng(points)
    return {"data": data, "geodesic": geodesic, "stroke_color": stroke_color, "stroke_opacity": stroke_opacity, "stroke_weight": stroke_weight }


def polyline_layer(points, geodesic=True, stroke_color="#FF0000", stroke_opacity=1.0, stroke_weight=2):
    """
    Create a polylines layer.

    Add this layer to a ``Map`` instance to draw polylines on the map.

    :Examples:

    >>> points = [(46.4, 6.9), (46.9, 8.0)]
    >>> directions = gmaps.polylines_layer(points)

    :param points:
        Iterable of (latitude, longitude) pair denoting points.
    :type waypoints: List of 2-element tuples, optional
    """
    widget_args = _polyline_options(points, geodesic, stroke_color, stroke_opacity, stroke_weight)
    return Polyline(**widget_args)
