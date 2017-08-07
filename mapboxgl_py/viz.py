from IPython.core.display import HTML, display
from .config import mapconfig
import json


class CircleViz(object):
    """Create a circle map"""

    def __init__(self, accessToken, div_id='map', width='100%', height='500px'):
        """Construct a Mapviz object

        :param access_token: Mapbox GL JS access token.
        :param div_id: The HTML div id of the map container in the viz
        :param width: The CSS width of the HTML div id in % or pixels.
        :param height: The CSS height of the HTML map div in % or pixels.
        """
        self.accessToken = accessToken
        self.div_id = div_id
        self.width = width
        self.height = height
        self.html_data = ''

    def as_iframe(self):
        """Build the HTML representation for the mapviz."""

        srcdoc = self.html_data.replace('"', "'")
        return ('<iframe id="{div_id}", srcdoc="{srcdoc}" style="width: {width}; '
                'height: {height}; border: none"></iframe>'.format(
                    div_id=self.div_id,
                    srcdoc=srcdoc,
                    width=self.width,
                    height=self.height)
                )

    def displayViz(self, html_data):
        # Load the HTML iframe
        map_html = self.as_iframe()

        # Display the iframe in the current jupyter notebook view
        display(HTML(map_html))

    def createLegend():
        """ Generate an HTML legend for a viz"""
        pass

    def as_image():
        """ Export a map visual to a static image """
        pass

    def createViz(self, 
                    data, 
                    colorProperty=None, 
                    colorStops=None,
                    styleUrl="mapbox://styles/mapbox/light-v9",
                    center=None, 
                    zoom=None):
        """Create a circle visual from a geojson data source"""
        if not colorProperty:
            colorProperty = ''
        if not center:
            center = [0,0]
        if not zoom:
            zoom = 0
        if not colorStops:
            colorStops = [[0,'red'], [100, 'green']]

        self.html_data = mapconfig.HTML_HEAD + mapconfig.HTML_CIRCLE_VIZ.format(
                            accessToken=self.accessToken,
                            div_id=self.div_id,
                            styleUrl=styleUrl,
                            center=center,
                            zoom=zoom,
                            geojson_data=json.dumps(data, ensure_ascii=False),
                            colorProperty=colorProperty,
                            colorStops=colorStops
                         ) + mapconfig.HTML_TAIL

        self.displayViz(self.html_data)

    def as_HTML(self):
        """ Return the HTML used to create the viz"""
        return self.html_data

    def getToken(self):
        """ Return the Mapbox access token used in the viz """
        return self.accessToken

