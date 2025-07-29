from dash import html, hooks, Input, Output, State, dcc
import dash_bootstrap_components as dbc

# Function to register hooks
def customize_app_selectors():
    return  html.Div([

                #Collapse button
                dbc.Button( "Customizable App Style",
                    id          = "style_btn",
                    n_clicks    = 0,
                    type        = "button",
                    class_name  = "btn btn-success text-center m-1 p-1 fs-6 .small"),

                dbc.Collapse(dbc.Card(
                    children    = [
                        html.Div(
                            children = [
                                # Label for backgruond color picker
                                html.Label( "App color mode:",
                                    style   = { "padding":      "1px",
                                                "padding-left": "5px",
                                                "fontSize":     12}),

                                # Background color picker from Dash Bootstrap Components
                                dbc.Input(
                                    id      = "bg_color",
                                    type    = "color",
                                    value   = "#FFFFFF",
                                    style   = { "width":        "200px",
                                                "padding":      "1px",
                                                "fontSize":     12}),

                                # Label for text color picker
                                html.Label( "App text color:",
                                    style   = { "padding":      "1px",
                                                "padding-left": "5px",
                                                "fontSize":     12}),

                                # Text color picker from Dash Bootstrap Components
                                dbc.Input(
                                    id      = "text_color",
                                    type    = "color",
                                    value   = "#000000",
                                    style   = { "width":        "200px",
                                                "padding":      "1px",
                                                "fontSize":     12}),

                                # Label for font type
                                html.Label( "App text color:",
                                    style   = { "padding":      "1px",
                                                "padding-left": "5px",
                                                "fontSize":     12}),

                                # Text color picker from Dash Bootstrap Components
                                dcc.Dropdown(
                                    id      = "font_type",
                                    options = [ "Times New Roman", "Georgia", "Arial",
                                                "Verdana", "Helvetica", "Courier New",
                                                "Lucida Console", "Monaco"],
                                    value   = "Arial",
                                    style   = { "width":    "200px",
                                                "padding":  "1px",
                                                "fontSize": 12})
                            ], style    = { "display":          "flex",
                                            "justify-content":  "left",
                                            "align-items":      "center"})                                
                    ]),

                    id          = "style_collapse",
                    is_open     = False,
                    class_name  = "W-100",
                ),

            ], style = {"backgroundColor":  "#FFFFFF",
                        "color":            "black"})

@hooks.callback(
    Output("main_container",    "style"),
    [Input("bg_color",          "value"),
    Input("text_color",         "value"),
    Input("font_type",          "value")]
)
def update_style(bg_color, text_color, font_type):

    # Return the style dict for the main cnontainer of the app
    return {
        "minHeight":            "100vh",
        "backgroundColor":      bg_color,
        "color":                text_color,
        "font-family":          font_type,
        "transition":           "background-color 0.3s"
    }


@hooks.callback(
    Output("style_collapse",    "is_open"),
    Input("style_btn",          "n_clicks"),
    [State("style_collapse",    "is_open")]
)
def toggle_app_style_collapse(n1, is_open):
    if n1:
        return not is_open
    return is_open