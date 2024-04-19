import numpy as np
import plotly.graph_objects as go

class AwfulCharts:
    def __prepare_grid__(self, start_angle: (int | float), end_angle: (int | float), amount_radius: int, angle_multiplyer: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        angles = np.linspace(0, 90, amount_radius)
        radius = np.cos(np.radians(angles))

        amount_of_angles = (end_angle - start_angle) * angle_multiplyer

        phi = np.radians(np.linspace(start_angle, end_angle, amount_of_angles))
        phi, radius = np.meshgrid(phi, radius)

        x = radius * np.cos(phi)
        y = radius * np.sin(phi)
        z = np.sqrt(1.000001 - np.power(x, 2) - np.power(y, 2)) 

        return x, y, z
    
    def __make_scatter_sector__(self, color, marker_size, **kwargs) -> list[go.Scatter3d, go.Scatter3d]:
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
                )
            ),
            go.Scatter3d(
                x=x.flatten(),
                y=y.flatten(),
                z=-z.flatten(),
                mode='markers',
                marker=dict(
                    size=marker_size,
                    color=color
                )
            )
        ]
        return sector
    
    def __make_surface_sector__(self, color, **kwargs):
        x, y, z = self.__prepare_grid__(**kwargs)
        colorscale = [[0, color], [1, color]]
        sector = [
            go.Surface(
                x=x,
                y=y,
                z=z,
                colorscale = colorscale
            ),
            go.Surface(
                x=x,
                y=y,
                z=-z,
                colorscale = colorscale
            )
        ]
        return sector

    def __make_sector__(self, method, color, marker_size=None, **kwargs):
        if method == 'surface':
            sector = self.__make_surface_sector__(color, **kwargs)

        elif method == 'scatter':
            sector = self.__make_scatter_sector__(color, marker_size, **kwargs)

        else:
            raise ValueError("Unknown method (must be <<surface>> or <<scatter>>)")
        
        return sector

    def watermelon(self, amount_of_sectors=20, amount_radius=20, angle_multiplyer=2, marker_size=5, method='surface', show=True):    
        tick = 1
        figures = []
        for i in range(amount_of_sectors):
            start_angle = 360//amount_of_sectors * i
            end_angle = 360//amount_of_sectors * (i+1)
            color = 'darkgreen' if tick == 1 else 'lightgreen'
            
            current_sector = self.__make_sector__(method, 
                                                  color, 
                                                  marker_size, 
                                                  start_angle=start_angle, 
                                                  end_angle=end_angle, 
                                                  amount_radius=amount_radius,
                                                  angle_multiplyer=angle_multiplyer
                                                  )
            figures += current_sector

            tick *= -1
        fig = go.Figure(data=figures)
        fig.update_layout(
            scene=dict(
                aspectmode='manual',
                aspectratio=dict(x=1, y=1, z=1),
                xaxis=dict(range=[-1, 1]),  # Лимиты для оси X
                yaxis=dict(range=[-1, 1]),  # Лимиты для оси Y
                zaxis=dict(range=[-1, 1]),  # Лимиты для оси Z
            )
        )
        fig.show()

if __name__ == '__main__':
    chart = AwfulCharts()
    chart.watermelon()