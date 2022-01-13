import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D
import numpy as np
from astropy.time import Time
from spacepy.constants import *

def num2str(number):
    if number < 10:
        return '0' + str(number)
    else:
        return str(number)

class Render2D:
    def __init__(self, system_name, star):
        plt.rcParams['figure.facecolor'] = SPACE_COLOR
        self.figure = plt.figure(figsize=[10, 10])
        self.figure.canvas.set_window_title(system_name)
        self.axes = plt.axes(xlim=(-8, 8), ylim=(-8, 8))
        self.axes.set_aspect('equal')
        self.axes.axis('off')

        self.time_stamps_x = np.zeros((2, 2))
        self.time_stamps_y = np.zeros((2, 2))

        self.patches = []

        self.lines = []

        self.labels = []
        self.star = star
        self.timetext = self.axes.text(-6, 6, '', color='white')

    def animation_init(self):
        for ii in range(0, len(self.lines)):
            self.lines[ii].set_data([], [])
            self.patches[ii].center = (self.time_stamps_x[0, ii], self.time_stamps_y[0, ii])
            self.axes.add_patch(self.patches[ii])
        self.actual_day = Time(self.initial_day)
        return tuple(self.lines) + tuple(self.patches)

    def animate(self, i):
        actual_date = self.actual_day.to_value('datetime')
        self.timetext.set_text(f'Date: {num2str(actual_date.day)} - {num2str(actual_date.month)} - {actual_date.year}')
        for jj in range(0, len(self.lines)):
            x = self.time_stamps_x[0:i, jj]
            y = self.time_stamps_y[0:i, jj]
            self.lines[jj].set_data(x, y)

            self.patches[jj].center = (self.time_stamps_x[i, jj], self.time_stamps_y[i, jj])
        self.actual_day += 1
        return tuple(self.lines) + tuple(self.patches) + (self.timetext,)

    def display(self, star, planets, states_time_stamps, initial_day, days):
        self.actual_day = Time(initial_day)
        self.initial_day = initial_day
        matrices = self.__generate_matrix(states_time_stamps)
        self.time_stamps_x = matrices[0]
        self.time_stamps_y = matrices[1]

        self.labels.append(Line2D([0], [0], marker='o', color=SPACE_COLOR, label=self.star.name,
                                  markerfacecolor=self.star.color, markersize=15))
        for ii in range(0, len(planets)):
            self.lines.append(self.axes.plot([], [], lw=2, color=planets[ii].color)[0])
            self.patches.append(plt.Circle((self.time_stamps_x[0, ii], self.time_stamps_y[0, ii]),
                                           0.05, color=planets[ii].color))
            self.labels.append(Line2D([0], [0], marker='o', color=SPACE_COLOR, label=planets[ii].name,
                                      markerfacecolor=planets[ii].color, markersize=15))
        self.legenda = plt.legend(handles=self.labels)
        for text in self.legenda.get_texts():
            text.set_color('white')
        frame = self.legenda.get_frame()
        frame.set_facecolor(SPACE_COLOR)
        frame.set_edgecolor(SPACE_COLOR)
        # Display the star:
        star_circle = plt.Circle((star.actual_state.pos[0], star.actual_state.pos[1]), 0.1, color=star.color)
        self.axes.add_patch(star_circle)



        self.animation = animation.FuncAnimation(self.figure, self.animate, init_func=self.animation_init,
                                                 frames=days, interval=20, blit=True)
        plt.show()

    def __generate_matrix(self, states_time_stamps):
        row = len(states_time_stamps)
        col = len(states_time_stamps[0])
        matrix_x = np.zeros((row, col))
        matrix_y = np.zeros((row, col))
        for r in range(0, row):
            for c in range(0, col):
                matrix_x[r, c] = states_time_stamps[r][c].pos[0]
                matrix_y[r, c] = states_time_stamps[r][c].pos[1]
        return (matrix_x, matrix_y)


