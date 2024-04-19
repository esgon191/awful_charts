import numpy as np
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import random
class AwfulCharts:
    def __init__(self, amount_radius=20, angle_multiplyer=2):
        self.amount_radius=amount_radius
        self.angle_multiplyer=angle_multiplyer

    def __prepare_grid__(self, start_angle: (int | float), end_angle: (int | float)) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        angles = np.linspace(0, 90, self.amount_radius)
        radius = np.cos(np.radians(angles))

        amount_of_angles = (end_angle - start_angle) * self.angle_multiplyer

        phi = np.radians(np.linspace(start_angle, end_angle, int(amount_of_angles)))
        phi, radius = np.meshgrid(phi, radius)

        x = radius * np.cos(phi)
        y = radius * np.sin(phi)
        z = np.sqrt(1.000001 - np.power(x, 2) - np.power(y, 2)) 

        return x, y, z
    
    def __make_scatter_sector__(self, color='black', name='долька', marker_size=5, **kwargs) -> list[go.Scatter3d, go.Scatter3d]:
        x, y, z = self.__prepare_grid__(**kwargs)
        sector = [
            go.Scatter3d(
                x=x.flatten(),
                y=y.flatten(),
                z=z.flatten(),
                mode='markers',
                marker=dict(
                    size=marker_size,
                    color=color
                ),
                name=name
            ),
            go.Scatter3d(
                x=x.flatten(),
                y=y.flatten(),
                z=-z.flatten(),
                mode='markers',
                marker=dict(
                    size=marker_size,
                    color=color
                ),
                name=name
            )
        ]
        return sector
    
    def __make_surface_sector__(self, color='black', name='долька',  **kwargs) -> list[go.Scatter3d, go.Scatter3d]:
        x, y, z = self.__prepare_grid__(**kwargs)
        colorscale = [[0, color], [1, color]]
        sector = [
            go.Surface(
                x=x,
                y=y,
                z=z,
                colorscale = colorscale,
                name=name,
                showscale=False,
                showlegend=False
            ),
            go.Surface(
                x=x,
                y=y,
                z=-z,
                colorscale = colorscale,
                name=name,
                showscale=False
            )
        ]
        return sector

    def __make_sector__(self, method, **kwargs):
        if method == 'surface':
            sector = self.__make_surface_sector__(**kwargs)

        elif method == 'scatter':
            sector = self.__make_scatter_sector__(**kwargs)

        else:
            raise ValueError("Unknown method (must be <<surface>> or <<scatter>>)")
        
        return sector
    
    def __make_sectors__(self, angles : list, colors : list, method : str, names : list=None, **kwargs) -> list[go.Scatter3d]:
        sectors = []
        current_angle = 0
        if names == None:
            names = [None for _ in angles]

        for angle, name, color in zip(angles, names, colors):
            sector = self.__make_sector__(
                                        method, 
                                        color=color, 
                                        name=name, 
                                        start_angle=current_angle, 
                                        end_angle=current_angle+angle
                                        )
            sectors+=sector
            current_angle+=angle
        return sectors

    def __legend__(self, fig: go.Figure, colors: list, names: list) -> go.Figure:
        for i, (legend, color) in enumerate(zip(names, colors)):
            fig.add_annotation(xref='paper', x=0.03, y=1-i*0.05, text=legend,
                            showarrow=False, xanchor='left', yanchor='middle',
                            font=dict(size=12, color=color))

            # Добавление символов легенды (квадратики)
            fig.add_shape(type='rect', xref='paper', yref='paper',
                        x0=0, y0=0.99-i*0.05-0.015, x1=0.02, y1=0.99-i*0.05+0.015,
                        line=dict(color=color), fillcolor=color)
            
        return fig

    def __generate_colors__(self, n):
        css_colors = [
            "AliceBlue", "AntiqueWhite", "Aqua", "Aquamarine", "Azure",
            "Beige", "Bisque", "Black", "BlanchedAlmond", "Blue",
            "BlueViolet", "Brown", "BurlyWood", "CadetBlue", "Chartreuse",
            "Chocolate", "Coral", "CornflowerBlue", "Cornsilk", "Crimson",
            "Cyan", "DarkBlue", "DarkCyan", "DarkGoldenRod", "DarkGray",
            "DarkGrey", "DarkGreen", "DarkKhaki", "DarkMagenta", "DarkOliveGreen",
            "Darkorange", "DarkOrchid", "DarkRed", "DarkSalmon", "DarkSeaGreen",
            "DarkSlateBlue", "DarkSlateGray", "DarkSlateGrey", "DarkTurquoise", "DarkViolet",
            "DeepPink", "DeepSkyBlue", "DimGray", "DimGrey", "DodgerBlue",
            "FireBrick", "FloralWhite", "ForestGreen", "Fuchsia", "Gainsboro",
            "GhostWhite", "Gold", "GoldenRod", "Gray", "Grey",
            "Green", "GreenYellow", "HoneyDew", "HotPink", "IndianRed", 
            "Indigo", "Ivory", "Khaki", "Lavender", "LavenderBlush", 
            "LawnGreen", "LemonChiffon", "LightBlue", "LightCoral", "LightCyan",
            "LightGoldenRodYellow", "LightGray", "LightGrey", "LightGreen", "LightPink", 
            "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSlateGrey",
            "LightSteelBlue", "LightYellow", "Lime", "LimeGreen", "Linen",
            "Magenta", "Maroon", "MediumAquaMarine", "MediumBlue", "MediumOrchid",
            "MediumPurple", "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise",
            "MediumVioletRed", "MidnightBlue", "MintCream", "MistyRose", "Moccasin",
            "NavajoWhite", "Navy", "OldLace", "Olive", "OliveDrab",
            "Orange", "OrangeRed", "Orchid", "PaleGoldenRod", "PaleGreen",
            "PaleTurquoise", "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru",
            "Pink", "Plum", "PowderBlue", "Purple", "Red",
            "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", "SandyBrown",
            "SeaGreen", "SeaShell", "Sienna", "Silver", "SkyBlue",
            "SlateBlue", "SlateGray", "SlateGrey", "Snow", "SpringGreen",
            "SteelBlue", "Tan", "Teal", "Thistle", "Tomato",
            "Turquoise", "Violet", "Wheat", "White", "WhiteSmoke",
            "Yellow", "YellowGreen"
        ]

        colors = random.sample(css_colors, n)  
        return colors

    def watermelon(self, amount_of_sectors=20, marker_size=5, method='surface', show=True):    
        angles = [360/amount_of_sectors for _ in range(amount_of_sectors)]
        colors = [('darkgreen', 'lightgreen')[i%2] for i in range(amount_of_sectors)]
        
        sectors = self.__make_sectors__(angles, colors, method, marker_size=marker_size)

        fig = go.Figure(data=sectors)
        #fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
        #fig.update_traces(showlegend=True)

        names=['долька' for _ in range(amount_of_sectors)]
        fig = self.__legend__(fig, colors, names)
        fig.update_layout(
            title='Диаграмма арбуза'
        )

        if show:
            fig.show()

        else:
            return fig
        
    def watermelon_chart(self, data: pd.DataFrame, names: str, values: str, title: str=None, method='surface', sort=True, show=True):
        data = data.copy()
        if sort:
            data.sort_values(by=values, inplace=True)

        angles = (data[values] * (360 / data[values].sum())).tolist()
        colors = self.__generate_colors__(len(angles))
        sectors = self.__make_sectors__(angles, colors, method, names)

        fig = go.Figure(sectors)
        fig = self.__legend__(fig, colors, data[names].to_list())

        if title != None:
            fig.update_layout(
                title=title
            )
        
        if show:
            fig.show()

        else:
            return fig

if __name__ == '__main__':
    chart = AwfulCharts()
    data = pd.DataFrame({
        'names' : ['alpha', 'beta', 'gamma', 'sigma'],
        'values' : [10, 40, 20, 80]
    })
    chart.watermelon_chart(data=data, names='names', values='values', title='хуй')