# mapboxgl-jupyter

Create [Mapbox GL JS](https://www.mapbox.com/mapbox-gl-js/api/) data visualizations natively in your Jupyter Notebook workflows with Python and Pandas dataframes.

## Python Library

Use the `mapboxgl_viz` python library in the `/python` directory to create a viz directly from a python data object or Pandas dataframe.  Work in progress.

## Running Example

1. Install Python3.4+
2. cd to /example directory of mapboxgl-jupyter repo
2. `pip install jupyter`
3. `jupyter notebook`
4. Open `jupyter-mapboxgl-example` workbook
5. Put your [Mapbox GL Access Token](https://www.mapbox.com/help/how-access-tokens-work/) (it's free for developers!) into cell 214 in the workbook
6. Run all cells in the notebook
7. View the location viz in the notebook in the final cell
    * ![](https://cl.ly/1r2s2t2Z2N0p/download/Image%202017-07-27%20at%203.06.54%20PM.png)

## Using

1. Pipe in your data analysis from a dataframe.
2. Edit the `html_data` using any [Mapbox GL JS](https://www.mapbox.com/mapbox-gl-js/api/) javascript code.

#### Notes on Mapbox Atlas

If you have access to Mapbox Atlas Server on your enterprise network, simply pass in your map stylesheet from your local Atlas URL as opposed to a `mapbox://` URL in cell 214.

```
# Put your Your Mapbox Access token here
# https://www.mapbox.com/help/how-access-tokens-work/
# If you use Mapbox Atlas, this isn't required.  Leave as an empty string.
mapbox_accesstoken = ''

# Map Style.  Point this to a local style, or a custom style on your Mapbox account or Atlas instance
mapStyle = "myAtlasUrl:myAtlasPort:/myStylesheetLocaiton"
```

