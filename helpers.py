#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


def generate(n_trial=None,
             max_pump=None,
             balloon_number=1
             ):
    """
    Generate exp data.
    Returns the DataFrame contains the stimulus

    Parameters
    ----------
    n_trial : int
        number of trials per balloon
    max_pump : int
        maximum number of pumps per balloon
    balloon_number : int
        number of balloons in the experiment: 1

    Returns
    -------
    df : DataFrame
    """
    if n_trial is None:
        n_trial = 30
    if max_pump is None:
        max_pump = 128

    df = pd.DataFrame()
    df['max_pump'] = [max_pump]*n_trial
    bp = np.random.randint(1, max_pump, n_trial)
    while abs(np.mean(bp)-max_pump/2)>=3:
        bp = np.random.randint(1, max_pump, n_trial)
    df['break_point'] = bp

    return df


class Button:
    '''
    button class
    '''
    def __init__(self, text, shape, pos=None, size=None):
        """
        Parameters
        ----------
        text : visual.TextStim
            text for values or probabilities
        shape : visual.ShapeStim
            shape for the cell in the table
        pos : np.array
            button position
        size : np.array
            button size
        """
        self.txt = text
        self.shape = shape
        if pos is not None:
            self.pos = pos
            self.shape.pos = self.size
            self.txt.pos = self.pos
        else:
            self.pos = None
        if size is not None:
            self.size = size
            self.shape.size = self.size
        else:
            self.size = None

    def set_pos(self, pos, size):
        self.pos = pos
        self.size = size
        self.shape.pos = self.pos
        self.shape.size = self.size
        self.txt.pos = self.pos

    def draw(self):
        self.txt.draw()
        self.shape.draw()


class Balloon:
    def __init__(self, img, shape, size=None, bottom_pos=None):
        """
        Parameters
        ----------
        img : visual.ImageStim
            image for balloon
        shape : visual.ShapeStim
            shape for balloon
        size : int
            balloon size
        bottom_pos : np.array
            balloon position
        """
        self.img = img
        self.shape = shape
        self.size0 = size
        self.size = size
        self.bottom_pos = bottom_pos
        self.pos = bottom_pos+np.array([0, self.size/2])
        self.img.pos = self.pos
        self.img.size = self.size
        self.n_pump = 0

    def pump(self, r_change=1):
        self.n_pump += 1
        self.size += r_change
        self.pos = self.bottom_pos + np.array([0, self.size/2])
        self.img.pos = self.pos
        self.img.size = self.size

    def reset(self):
        self.n_pump = 0
        self.size = self.size0
        self.pos = self.bottom_pos + np.array([0, self.size / 2])
        self.img.pos = self.pos
        self.img.size = self.size

    def draw(self):
        self.shape.draw()
        self.img.draw()




