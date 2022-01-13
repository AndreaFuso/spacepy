import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Render2D:
    def __init__(self, system_name):
        plt.rcParams['figure.facecolor'] = '#1D3557'
        self.figure = plt.figure(figsize=[10, 10])
        self.figure.canvas.set_window_title(system_name)
        self.axes = plt.axes(xlim=(-8, 8), ylim=(-8, 8))
        self.axes.set_aspect('equal')
        self.axes.axis('off')

    def display(self, star, planets, states_time_stamps):
        # Display the star:
        star_circle = plt.Circle((star.actual_state.pos[0], star.actual_state.pos[1]), 0.1, color=star.color)
        self.axes.add_patch(star_circle)
        # Displaying planets:
        for ii in range(0, len(states_time_stamps[0])):
            self.axes.add_patch(plt.Circle((states_time_stamps[0][ii].pos[0],
                                            states_time_stamps[0][ii].pos[1]),
                                           0.05, color=planets[ii].color))
        plt.show()

