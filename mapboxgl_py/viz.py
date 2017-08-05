from IPython.core.display import HTML, display
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


    def repr_html(self, html_data):
        """Build the HTML representation for the mapviz."""

        srcdoc = html_data.replace('"', "'")
        return ('<iframe id={div_id}, srcdoc="{srcdoc}" style="width: {width}; '
                'height: {height}; border: none"></iframe>'.format(
                    div_id=self.div_id, 
                    srcdoc=srcdoc, 
                    width=self.width,
                    height=self.height)
                    )

    def getToken(self):
        return self.accessToken


    def createViz(self, data, vizProperty, styleUrl="mapbox://styles/mapbox/light-v9",
                 center=[0, 0], zoom=0, colorStops=None):
        """Create a circle visual from a geojson data source"""

        if not colorStops:
            colorStops = [
                [1000, '#2b83ba'],
                [3000, '#abdda4'],
                [6000, '#ffffbf'],
                [9000, '#fdae61'],
                [12000, '#d7191c']
            ]
        else:
            colorStops = colorStops

        html_data = """
        <!DOCTYPE html><html>
            <head>
                <meta charset='utf-8' />
                <title></title>
                <meta name='viewport' content='initial-scale=1,maximum-scale=1,user-scalable=no' />
                <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v0.39.1/mapbox-gl.js'></script>
                <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v0.39.1/mapbox-gl.css' rel='stylesheet' />
                    <style>
                    body {{ margin:0; padding:0; }}
                    #map {{ position:absolute; top:0; bottom:0; width:100%; }}
                    .mapboxgl-popup-content {{
                        margin-left: 5px;
                        margin-top: 2px;
                        margin-bottom: 2px;
                        margin-right: 5px;
                        z-index: 1000;
                    }}
                </style>
            </head>
            <body>
            <div id='map'></div>
            <script>

                // This is where we insert our Mapbox Accesstoken.  
                // If you are using an onprem Mapbox Atlas instance, this is not needed
                mapboxgl.accessToken = '{accessToken}';

                // Load the map
                var map = new mapboxgl.Map({{
                    container: 'map', // container id
                    style: '{styleUrl}', // map style from python variable
                    center: {center}, // starting position of map from python variable
                    zoom: {zoom} // starting zoom from python variable
                }});

                // Add our data for viz when the map loads
                map.on('load', function() {{
                    
                    // Add the source geojson data from our dataframe
                    map.addSource("data", {{
                        "type": "geojson",
                        "data": {geojson_data}, //data from dataframe output to geojson
                        "buffer": 1,
                        "maxzoom": 14
                    }})
                    
                    // Here's our layer
                    map.addLayer({{
                        "id": "circle",
                        "source": "data",
                        "type": "circle",
                        "paint": {{
                            // Use Data-Driven Styles to make color represent a data property
                            "circle-color": {{
                                "property": "{vizProperty}", //Data property to style color by from python variable
                                "stops": {colorStops}  // Color stops array to use based on data values from python variable
                            }},
                            // Use Zoom-Driven Styles to control the size of circles based on zoom
                            "circle-radius" : {{
                                "stops": [[0,1], [18,10]]
                            }},
                            "circle-stroke-color": "white",
                            "circle-stroke-width": {{
                                "stops": [[0,0.01], [18,1]]
                            }}
                        }}
                    }}, "waterway-label");
                    
                    // Create a popup
                    var popup = new mapboxgl.Popup({{
                        closeButton: false,
                        closeOnClick: false
                    }});
                    
                    // Show the popup on mouseover
                    map.on('mousemove', 'circle', function(e) {{
                        // Change the cursor style as a UI indicator.
                        map.getCanvas().style.cursor = 'pointer';

                        // Populate the popup and set its coordinates
                        // based on the feature found.
                        popup.setLngLat(e.features[0].geometry.coordinates)
                            .setHTML('<li> {vizProperty}: $' + e.features[0].properties["{vizProperty}"] + '</li>')
                            .addTo(map);
                    }});

                    map.on('mouseleave', 'circle', function() {{
                        map.getCanvas().style.cursor = '';
                        popup.remove();
                    }});
                    
                    // Fly to on click
                    map.on('click', 'circle', function(e) {{
                        map.flyTo({{
                            center: e.features[0].geometry.coordinates,
                            zoom: 10
                        }});
                    }});
                }});
                </script>
            </body>
        </html>""".format(
            accessToken=self.accessToken,
            styleUrl=styleUrl,
            center=center,
            zoom=zoom,
            geojson_data=json.dumps(data),
            vizProperty=vizProperty,
            colorStops=colorStops
        )

        return html_data

    def displayViz(self, html_data):
        # Load the HTML iframe
        map_html = self.repr_html(html_data)

        # Display the iframe in the current jupyter notebook view
        display(HTML(map_html))
