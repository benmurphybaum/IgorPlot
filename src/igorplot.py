import numpy as np
import matplotlib.figure
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.lines as lines
from matplotlib.axes import Axes

from src import testplot

import igorpro

markerDict: dict[str,int] = {
    'o': 19,   # filled circle
    's': 16,   # filled square
    '^': 17,   # up triangle
    'v': 23,   # down triangle
    '<': 46,   # left triangle
    '>': 49,   # right triangle
    'p': 52,   # pentagon
    '8': 55,   # octagon (Igor doesn't have this, sub hexagon)
    'h': 55,   # hexagon 1
    'H': 55,   # hexagon 2
    'd': 29,   # thin diamond
    'D': 18,   # diamond
    '|': 10,   # vertical line
    '_': 9,    # horizontal line
    'x': 1,    # x
    '+': 0,    # +
    '*': 60,   # star
    '1': 58,   # tri_down (Igor only has tri_up)
    '2': 58,   # tri_up (Igor only has tri_up)
    '3': 58,   # tri_left (Igor only has tri_up)
    '4': 58,   # tri_right (Igor only has tri_up)
    }

lineStyleDict: dict[str,int] = {
    '-': 0,         # solid
    'solid': 0,     # solid
    '--': 3,        # dashed
    'dashed': 3,    # dashed
    '-.': 5,        # dash dot
    'dashdot': 5,   # dash dot
    ':': 1,         # dotted
    'dotted': 1,    # dotted
}

def get_igor_marker(marker: str) -> int:
    return markerDict.get(marker, 19) # filled circle is a good default marker

def get_igor_linestyle(style: str) -> int:
    return lineStyleDict.get(style, 0) # default to solid line

def linePlot(axis : Axes) -> list[str]:
    """
    Generates a line plot in Igor Pro from an input matplotlib axis object.

    Parameters
    ----------
    axis : matplotlib.axes.Axes
        Axis to plot

    Returns
    -------
    List of the wave names that were appended to the graph
    """

    xLimits = axis.get_xlim()
    yLimits = axis.get_ylim()

    xLabel = axis.get_xlabel()
    yLabel = axis.get_ylabel()

    i = 0
    waveNameList: list = []
    for trace in axis.get_lines():

        # Line data
        xdata = trace.get_xdata()
        ydata = trace.get_ydata()

        xWave = igorpro.wave.createfrom(f'xWave_{i}', xdata, overwrite=True)
        yWave = igorpro.wave.createfrom(f'yWave_{i}', ydata, overwrite=True)

        yWaveName = yWave.name()
        xWaveName = xWave.name()

        waveNameList.append(yWaveName)

        igorpro.execute(f'AppendToGraph {yWaveName} vs {xWaveName}')

        # Axis limits        
        igorpro.execute(f'SetAxis bottom {xLimits[0]}, {xLimits[1]}')
        igorpro.execute(f'SetAxis left {yLimits[0]}, {yLimits[1]}')

        # Axis labels
        igorpro.execute(f'Label bottom "{xLabel}"')
        igorpro.execute(f'Label left "{yLabel}"')

        # Grid lines
        gridLines = axis.get_xgridlines()
        if gridLines and gridLines[0].get_visible():
            gridRGBA = colors.to_rgba(gridLines[0].get_color())
            gridLineThick = gridLines[0].get_linewidth()
            igorpro.execute(f"""ModifyGraph grid(bottom) = 1, gridHair(bottom) = {gridLineThick}, gridStyle(bottom) = 3, 
                            gridRGB(bottom) = ({0xffff * gridRGBA[0]}, {0xffff * gridRGBA[1]}, {0xffff * gridRGBA[2]})""")
        
        gridLines = axis.get_ygridlines()
        if gridLines and gridLines[0].get_visible():
            gridColor = colors.to_rgba(gridLines[0].get_color())
            gridLineThick = gridLines[0].get_linewidth()
            igorpro.execute(f"""ModifyGraph grid(left) = 1, gridHair(left) = {gridLineThick}, gridStyle(left) = 3, 
                            gridRGB(left) = ({0xffff * gridRGBA[0]}, {0xffff * gridRGBA[1]}, {0xffff * gridRGBA[2]})""")

        # Line width
        lineWidth = trace.get_linewidth()
        igorpro.execute(f'ModifyGraph lsize({yWaveName})={lineWidth}')

        # Line style
        lineStyle = trace.get_linestyle()
        if lineStyle:
            igorpro.execute(f'ModifyGraph mode({yWaveName}) = 0, lstyle({yWaveName}) = {get_igor_linestyle(str(lineStyle))}')

        # Sparse markers
        markerEvery = trace.get_markevery()
        if markerEvery:
            igorpro.execute(f'ModifyGraph mode({yWaveName}) = 4, mskip({yWaveName}) = {markerEvery}, mSize({yWaveName}) = {trace.get_markersize()}')

        markerType = trace.get_marker()
        if markerType:
            igorpro.execute(f'ModifyGraph marker({yWaveName}) = {get_igor_marker(str(markerType))}')

        # Line color
        lineRGBA = colors.to_rgba(trace.get_color())
        igorpro.execute(f"""ModifyGraph  rgb({yWaveName}) = ({0xffff * lineRGBA[0]},
                        {0xffff * lineRGBA[1]},
                        {0xffff * lineRGBA[2]})""")

        i += 1

    return waveNameList

   

def convert(figure : matplotlib.figure.Figure):
    """
    Converts a matplotlib Figure into an Igor graph
    """

    igorpro.execute('Display')

    axes = figure.axes
    for axis in axes:
        if any(isinstance(line, lines.Line2D) for line in axis.get_lines()):
            waveNameList = linePlot(axis)
        else:
            print('Axis type not implemented:', axis)

    # Legend
    legend = figure.legend()
    legendCommand = 'Legend/C/N=legend/J "'
    if legend:
        labels = [text.get_text() for text in legend.get_texts()]
        
        nTraces = len(waveNameList)
        i = 0
        for label, name in zip(labels, waveNameList):
            if i < nTraces - 1:
                legendCommand += f'\\s({name}) {label}\\r'
            else:
                legendCommand += f'\\s({name}) {label}"'
            i += 1

        igorpro.execute(legendCommand)


if __name__ == '__main__':
    figure = testplot.createTestPlot()
    convert(figure)
