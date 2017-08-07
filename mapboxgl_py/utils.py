from collections import Mapping, Sequence
from .src import colorbrewer

def createColorStops(breaks, colors='RdYlGn'):
    """ Convert a list of breaks into color stops using colors from colorBrewer
        see www.colorbrewer2.org for a list of color options to pass
    """

    numBreaks = len(breaks)

    if not getattr(colorbrewer, colors):
        print ('color does not exist in colorBrewer!')
    elif numBreaks > 9:
        print ('choose fewer unique stops')
    else:
        stops = []
        for i, b in enumerate(breaks):
            stops.append([b, getattr(colorbrewer, colors)[numBreaks][i]])
        return stops

def normalize_geojson_featurecollection(obj):
    """Takes a geojson-like mapping representing
    geometry, Feature or FeatureCollection (or a sequence of such objects)
    and returns a FeatureCollection-like dict
    """
    if not isinstance(obj, Sequence):
        obj = [obj]

    features = []
    for x in obj:
        if not isinstance(x, Mapping) or 'type' not in x:
            raise ValueError(
                "Expecting a geojson-like mapping or sequence of them")

        if 'features' in x:
            features.extend(x['features'])
        elif 'geometry' in x:
            features.append(x)
        elif 'coordinates' in x:
            feat = {'type': 'Feature',
                    'properties': {},
                    'geometry': x}
            features.append(feat)
        else:
            raise ValueError(
                "Expecting a geojson-like mapping or sequence of them")

    return {'type': 'FeatureCollection', 'features': features}


def df_to_geojson(df, properties=[], lat='lat', lon='lon', precision=6):
    """Serialize a Pandas dataframe to a geojson format Python dictionary"""
    
    geojson = {'type':'FeatureCollection', 'features':[]}

    # Round geojson coordinate output to given precision
    df[lat] = df[lat].round(precision)
    df[lon] = df[lon].round(precision)

    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson