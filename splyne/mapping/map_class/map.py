import pandas as pd
import pydeck

from typing import Dict, Any, Union
from collections.abc import Iterable

from splyne.common.base import SplyneObject
from splyne.mapping.common.view_state import ViewState
from splyne.mapping.layers import scatterplot


class Map(SplyneObject):

    def __init__(self):
        super().__init__()
        self.viewState = ViewState()
        self.layers = []

    def make_iterable_of_dicts(
        self,
        data: Union[pd.DataFrame, Iterable[Dict[str, Any]]],
    ) -> Iterable[Dict[str, Any]]:
        if isinstance(data, pd.DataFrame):
            return data.to_dict('records')
        elif isinstance(data, Iterable):
            return data
        else:
            raise ValueError('Data must be a `pd.DataFrame` of `Iterable[Dict[str, Any]]`')

    def add_scatterplot_layer(
        self,
        data: Union[pd.DataFrame, Iterable[Dict[str, Any]]],
        **kwargs,
    ):
        data = self.make_iterable_of_dicts(data)
        layer = scatterplot.ScatterplotLayer(data, self.viewState, **kwargs)
        self.layers.append(layer.make_pydeck_layer())

    def display(self):
        chart = pydeck.Deck(
            layers=self.layers,
            initial_view_state=self.viewState.get_view_state(),
            map_style=pydeck.map_styles.LIGHT,
        )
        return chart.to_html('.splyne-tmp.html')


if __name__ == '__main__':
    map = Map()
    map.add_scatterplot_layer(
        data=[
            {'lat': 55.5, 'lon': 37.7, 'color': [255, 0, 0]},
            {'lat': 55.9, 'lon': 37.9, 'color': [0, 255, 0]},
            # {'lat': 89.0, 'lon': 179.0},
            # {'lat': -89.0, 'lon': -179.0},
        ],
        get_color='color',
    )
    map.display()