import json
import os
import pandas as pd
import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash import Dash, html, dcc, Output, Input
from dash_extensions.javascript import assign, arrow_function

# Obtener la ruta absoluta al archivo GeoJSON
geojson_path = os.path.abspath('Regiones.geojson')

# Cargar el archivo GeoJSON
with open(geojson_path, 'r') as f:
    geojson_data = json.load(f)

# Obtener la ruta del directorio base del proyecto
base_dir = os.getcwd()
data_dir = os.path.abspath(os.path.join(
    base_dir, '..', 'data', 'preprocessed'))

# Guardar el archivo en el directorio
file_path = os.path.join(data_dir, 'preprocessed_codificacion_eda.csv')

# Cargar el archivo CSV en un DataFrame
df = pd.read_csv(file_path)

# Convertir la columna 'CodigoEPH' a tipo entero en todo el GeoJSON
for feature in geojson_data['features']:
    feature['properties']['CodigoEPH'] = int(
        feature['properties']['CodigoEPH'])

# Agrupar datos por región.
variables = ['CH03', 'CH07', 'CH10', 'CH15', 'CH16', 'ESTADO']
df_agrupado = df.groupby('REGION')[variables].count().reset_index()

# Crear función para obtener información al pasar el cursor sobre una región.


def get_info(feature=None, variable='CH03'):
    header = [html.H4("Información de Regiones")]
    if not feature:
        return header + [html.P("Pasa el cursor sobre una región")]

    region_name = feature["properties"]["CodigoEPH"]
    region_data = df_agrupado[df_agrupado['REGION'] == region_name].iloc[0]

    info = [
        html.B(region_name), html.Br(),
        f"{variable}: {region_data[variable]:.3f}", html.Br(),
    ]
    return header + info


# Obtener los valores únicos de las variables para determinar las clases.
unique_values = df_agrupado[variables].stack().unique()
unique_values.sort()

# Definir las clases basadas en los valores únicos.
classes = list(unique_values)
colorscale = ['#FFEDA0', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C']
style = dict(weight=2, opacity=1, color='white',
             dashArray='3', fillOpacity=0.7)

# Create colorbar.
ctg = ["{}+".format(cls, classes[i + 1])
       for i, cls in enumerate(classes[:-1])] + ["{}+".format(classes[-1])]
colorbar = dlx.categorical_colorbar(
    categories=ctg, colorscale=colorscale, width=300, height=30, position="bottomleft")

# Función para asignar colores según los valores de la columna seleccionada en el DataFrame.
style_handle = assign("""
function(feature, context){
  const {classes, colorscale, style, colorProp} = context.hideout;
  const value = feature.properties[colorProp];

  if (typeof value !== 'number') {
    console.warn(`Invalid data type for colorProp: ${colorProp}. Expected a number.`);
    return style;
  }

  for (let i = 0; i < classes.length; ++i) {
    if (value < classes[i + 1]) {
      style.fillColor = colorscale[i];
      break;  // Exit loop after assigning color
    }
  }
  return style;
}
""")

# Create geojson.
geojson = dl.GeoJSON(
    data=geojson_data,
    style=style_handle,
    zoomToBounds=True,
    zoomToBoundsOnClick=True,
    hoverStyle=arrow_function(dict(weight=5, color='#666', dashArray='')),
    hideout=dict(colorscale=colorscale, classes=classes,
                 style=style, colorProp='CH03'),
    id="geojson"
)

# Crear la aplicación Dash.
app = Dash(prevent_initial_callbacks=True)
app.layout = html.Div([
    dcc.Dropdown(
        id='variable-dropdown',
        options=[{'label': col, 'value': col} for col in variables],
        value='CH03'
    ),
    dl.Map([
        dl.TileLayer(),
        geojson,
        colorbar  # Agregar el colorbar al layout
    ], style={'height': '50vh'}, center=[-34.6037, -58.3816], zoom=3),
    html.Div(id='info', className="info", style={
             "position": "absolute", "top": "10px", "right": "10px", "zIndex": "1000"})
])

# Callback para actualizar la información al seleccionar una variable.


@app.callback(Output("info", "children"), Input("geojson", "hoverData"), Input("variable-dropdown", "value"))
def update_info(feature, variable):
    return get_info(feature, variable)


if __name__ == '__main__':
    app.run_server(debug=True)
