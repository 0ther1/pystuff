from tkinter import *

class Plot():
    """Class representing a plot."""
    def __init__(self, name="New Plot", color="#000000", points=[], showpoints=True, showlines=True):
        """Create a new plot.
        [name] - name of this plot
        [color] - color of this plot lines and points
        [points] - points of this plot in format [(x, y), ...]
        [showpoints] - draw points or not
        [showlines] - draw lines or not"""
        self.name = name
        self.color = color
        self._points = points
        self.showpoints = showpoints
        self.showlines = showlines
    
    @property
    def points(self):
        return self._points.copy()
    
    @points.setter
    def points(self, value):
        """Get/set points list. Must be a list or tuple of list or tuples with two coordinates."""
        if (isinstance(value, list) or isinstance(value, tuple)):
            for e in value:
                if (not (isinstance(e, list) or isinstance(e, tuple))):
                    raise TypeError("Inside of containter of plots must be objects of class Plot!")
                else:
                    if (len(e) != 2):
                        raise ValueError("Each point must contain exactly two numbers - x and y!")
            self._points = list(value)
        else:
            raise TypeError("Points must be a list or a tuple!")
        
    def addPoint(self, point):
        """Add a new point to plot. 'point' must be list or tuple with two coordinates."""
        if (isinstance(point, list) or isinstance(point, tuple)):
            if (len(point) != 2):
                raise ValueError("Point must contain exactly two numbers - x and y!")
            self._points.append(tuple(point))
        else:
            raise TypeError("Points must be a list or a tuple!")        

class PlotDrawer(Frame):
    """Widget that can draw 2d plot on grid."""
    VERTICALS = 10      # count of vertical lines
    HORIZONTALS = 10    # count of horizontal lines
    
    def __init__(self, master, plots=[], scale=1, gridcolor="#BBBBBB", centercolor="#5555FF", **kw):
        """Create new PlotDrawer widget.
        master - parent widget
        [plots] - list of Plot objects
        [scale] - scale of the grid and plot
        [gridcolor] - color of grid
        [centercolor] - color of center (0, 0) of grid
        [kw] - additional tkinter options for Frame"""
        super().__init__(master, **kw)      # init base class
        W = 500                             # width of widget
        H = 500                             # height of widget
        if ("width" in kw.keys()):          # if width is given in kw
            W = kw["width"]                 # set given width
        if ("height" in kw.keys()):         # if height is given in kw
            H = kw["height"]                # set given height
        self._plots = plots                 # [INTERNAL] plot list
        self._scale = scale                 # [INTERNAL] grid and plot scale
        self._gridColor = gridcolor         # [INTERNAL] grid color
        self._centerColor = centercolor     # [INTERNAL] grid center color
        self._canvasW = W                   # [INTERNAL] width of canvas
        self._canvasH = H                   # [INTERNAL] height of canvas
        self._drawAxis = False              # [INTERNAL] visibility of axis NOT USED
        self._center = [0, 0]               # [INTERNAL] center of plot (in plot axis) (x,y)
        self._screenCenter = [W/2, H/2]     # [INTERNAL] center of plot (in screen axis) (x,y)
        self._steps = [0, 0]                # [INTERNAL] step of axis (x,y) NOT USED
        self._userScaled = False            # [INTERNAL] set if user changed scale
        self._lastMousePos = []             # [INTERNAl] last mouse position
        # Setup canvas
        bgcolor = "white"                   # background color of canvas
        if ("bg" in kw.keys()):             # if background color is given in kw
            bgcolor = kw["bg"]              # set given color
        self._canvas = Canvas(self, width=self._canvasW, height=self._canvasH, bg=bgcolor, highlightthickness=0)    # canvas for drawing
        self._canvas.grid(column=0, row=0, columnspan=20)       # place canvas 
        self._canvas.bind("<Motion>", self._showCooridnates)    # bind on mouse movement for canvas 
        self._canvas.bind("<B1-Motion>", self._moveGrid)        # bind on mouse drag for canvas
        self._canvas.bind("<MouseWheel>", self._changeScale)    # bind on mouse wheel for canvas
        self._canvas.bind("<Leave>", self._eraseCoordinates)    # bind on mouse leave for canvas
        self._canvas.bind("<Button-1>", lambda e: self._lastMousePos.extend([e.x, e.y]))
        self._canvas.bind("<ButtonRelease-1>", lambda e: self._lastMousePos.clear())    # bind on mouse button 1 release - clear last mousce position
        self._infoLabel = Label(self, text="X: --.------ ; Y: --.------")   # label for displaying coordinates
        self._infoLabel.grid(column=0, row=1)                   # place label
        self._scaleLabel = Label(self, text="Scale: %1.1f" % self.scale)    # label for displaying current scale
        self._scaleLabel.grid(column=19, row=1)
        self._drawGrid()                                        # begin drawing grid
        self._drawPoints()                                      # begin drawing points
        
    @property
    def scale(self):
        return self._scale
        
    @scale.setter
    def scale(self, value): 
        """Get/set scale of plot. Value must be in range (0, 10]."""
        if (value > 0 and value < 100):       # if value is valid
            if (value != self._scale):      # if value is not current scale
                self._scale = value    # set new scale
                self.update()               # update plot to redraw
        else:
            raise ValueError("Scale must be in range [1, 4]!")
        
    @property
    def plots(self):
        return self._plots.copy()
    
    @plots.setter
    def plots(self, value):
        """Get/set list of plots. Must be list or tuple of Plot objects."""
        if (isinstance(value, list) or isinstance(value, tuple)):
            for e in value:
                if (not isinstance(e, Plot)):
                    raise TypeError("Inside of containter of plots must be objects of class Plot!")
            self._plots = list(value)
        else:
            raise TypeError("Plots must be a list or a tuple!")
        
    def _changeScale(self, event):
        """[INTERNAL] handler for mouse wheel scaling."""
        if (not self._userScaled):
            self._userScaled = True
        try:
            self.scale += 0.5 if event.delta < 0 else -0.5  # try to change scale
        except ValueError:                                  # except invalid values 
            pass
        
    def _moveGrid(self, event):
        """[INTERNAL] handler for mouse canvas movement."""
        self._screenCenter[0] -= self._lastMousePos[0] - event.x
        self._screenCenter[1] -= self._lastMousePos[1] - event.y
        self._lastMousePos = [event.x, event.y]
        self.update()
        
    def _showCooridnates(self, event):
        """[INTERNAL] handler for displaying coordinates under pointer."""
        co = self._fromScreenCoordinates([event.x, event.y])                # convert pointer coordinates to plot axis
        for plot in self._plots:                                            # for every plot
            for p in plot.points:                                           # for every point
                if (abs(p[0] - co[0]) < 0.1 and abs(p[1] - co[1]) < 0.1):   # if pointer is near point
                    co = p                                                  # snap to this point
                    break
        self._infoLabel["text"] = "X: %.06f ; Y: %.06f" % (co[0], co[1])# display coordinates
        
    def _eraseCoordinates(self, event):
        """[INTERNAL] handler for displaying defalut value when coordinates cannot be received."""
        self._infoLabel["text"] = "X: --.------ ; Y: --.------"

    def _fromScreenCoordinates(self, point):
        """[INTERNAL] convert coordinates from screen to plot axis."""
        gridCountH = (self.HORIZONTALS*self._scale)     # count of horizontals
        gridCountV = (self.VERTICALS*self._scale)       # count of vertical
        gridWidth = self._canvasW / gridCountH          # width of one cell in grid
        gridHeight = self._canvasH / gridCountV         # height of one cell in grid
        screenCenter = [self._screenCenter[0] - self._center[0]*gridWidth, self._screenCenter[1] + self._center[1]*gridHeight]  # center of plot in screen coordinates
        return [(point[0] - screenCenter[0]) / gridWidth, -(point[1] - screenCenter[1]) / gridHeight]   # return converted coordinates
        
    def _toScreenCoordinates(self, point):
        """[INTERNAL] convert coordinates from plot to screen axis."""
        gridCountH = (self.HORIZONTALS*self._scale)     # count of horizontals
        gridCountV = (self.VERTICALS*self._scale)       # count of vertical
        gridWidth = self._canvasW / gridCountH          # width of one cell in grid
        gridHeight = self._canvasH / gridCountV         # height of one cell in grid
        screenCenter = [self._screenCenter[0] - self._center[0]*gridWidth, self._screenCenter[1] + self._center[1]*gridHeight] # center of plot in screen coordinates
        return [point[0]*gridWidth + screenCenter[0], screenCenter[1] - point[1]*gridHeight]    # return converted coordinates
        
    def _setupGrid(self):
        """[INTERNAL] prepare grid attributes."""
        X = []      # all x coordinates of all points
        Y = []      # all y coordinates of all points
        absX = []   # all absolute x coordinates of all points
        absY = []   # all absolute y coordinates of all points
        pointCount = 0                      # count of all points
        for plot in self._plots:            # for every plot
            pointCount += len(plot.points)
            for p in plot.points:           # for every point
                X.append(p[0])              # add x coordinate
                Y.append(p[1])              # add y coordinate
                absX.append(abs(p[0]))      # add absolute x coordinate
                absY.append(abs(p[1]))      # add absolute y coordinate
        if (pointCount > 0):
            self._center = [sum(X)/pointCount, sum(Y)/pointCount]   # calculate center of plot
            self._steps = [sum(absX) / self.HORIZONTALS, sum(absY) / self.VERTICALS]    # calculate step of grid
        
    def _drawGrid(self):
        """[INTERNAL] draw grid on canvas."""
        self._setupGrid()                           # prepare grid attributes
        self._canvas.delete(ALL)                    # clear canvas
        multiplier = (self._scale - 10*(self.scale//10))
        if (multiplier < 1):
            multiplier = 1
        gridCountH = int(self.HORIZONTALS*multiplier) # count of horizontals 
        gridCountV = int(self.VERTICALS*multiplier)   # count of verticals        
        gridWidth = self._canvasW / gridCountH      # width of one cell in grid
        gridHeight = self._canvasH / gridCountV     # height of one cell in grid
        cntr = self._toScreenCoordinates([0, 0])    # get center (0, 0) in screen coordinates
        lineY = cntr[1]
        sign = 1
        while (True):
            if (sign == 1):
                if (lineY > self._canvasH):
                    break
            else:
                if (lineY < 0):
                    break
            lineY += gridHeight * sign
            if (0 <= lineY <= self._canvasH):
                self._canvas.create_line(0, lineY, self._canvasW, lineY, fill=self._gridColor)
        lineY = cntr[1]
        sign = -1
        while (True):
            if (sign == 1):
                if (lineY > self._canvasH):
                    break
            else:
                if (lineY < 0):
                    break
            lineY += gridHeight * sign
            if (0 <= lineY <= self._canvasH):
                self._canvas.create_line(0, lineY, self._canvasW, lineY, fill=self._gridColor)  
        lineX = cntr[0]
        sign = 1
        while (True):
            if (sign == 1):
                if (lineX > self._canvasW):
                    break
            else:
                if (lineX < 0):
                    break
            lineX += gridWidth * sign
            if (0 <= lineX <= self._canvasW):
                self._canvas.create_line(lineX, 0, lineX, self._canvasW, fill=self._gridColor)
        lineX = cntr[0]
        sign = -1
        while (True):
            if (sign == 1):
                if (lineX > self._canvasW):
                    break
            else:
                if (lineX < 0):
                    break
            lineX += gridWidth * sign
            if (0 <= lineX <= self._canvasW):
                self._canvas.create_line(lineX, 0, lineX, self._canvasW, fill=self._gridColor)          
        if (0 <= cntr[0] <= self._canvasW):         # if x of center is within screen space - draw it
            self._canvas.create_line(cntr[0], 0, cntr[0], self._canvasH, fill=self._centerColor, width=2)
        if (0 <= cntr[1] <= self._canvasH):         # if y of center is within screen space - draw it
            self._canvas.create_line(0, cntr[1],self._canvasW, cntr[1], fill=self._centerColor, width=2)  
            
    def _drawPoints(self):
        """[INTERNAL] draw all points of plot."""
        pointSize = 4/((self.scale//10)+1)
        for plot in self._plots:
            lastPoint = None                        # previous point
            for p in plot.points:                   # for every point
                xy = self._toScreenCoordinates(p)   # convert point coordinates to screen space
                if (not self._userScaled):
                    if (0 > xy[0] or xy[0] > self._canvasW or 0 > xy[1] or xy[1] > self._canvasH):  # if point outside screen space
                        try:
                            self.scale += 0.1           # try to increase scale
                        except ValueError:              # excepting maximum scale
                            pass
                        break
                if (plot.showpoints):
                    self._canvas.create_oval(xy[0]-pointSize//2, xy[1]-pointSize//2, xy[0]+pointSize//2, xy[1]+pointSize//2, fill=plot.color, outline=plot.color) # draw point
                if (lastPoint):                     # if this is not first point of plot
                    xy2 = self._toScreenCoordinates(lastPoint)              # convert previous point coordinates to screen space
                    if (plot.showlines):
                        self._canvas.create_line(xy[0], xy[1], xy2[0], xy2[1], fill=plot.color, width=1*((self.scale//10)+1))  # draw line between previous and current points
                lastPoint = p                       # set current point as prevoius            
            
    def addPlot(self, plot):
        """Add a new plot to draw. 'plot' - a Plot object"""
        if (isinstance(plot, Plot)):    # if it's a Plot
            self._plots.append(plot)    # add it
            self.update()               # update to redraw
        else:
            raise TypeError("'plot' must be a Plot object!")
        
    def addPointToPlot(self, plotname, point):
        """Add new point to plot with name 'plotname'."""
        plot = None
        for plt in self._plots:
            if (plt.name == plotname):
                plot = plt
                break
        if (plot):
            plot.addPoint(point)
            self.update()
        else:
            raise ValueError("Plot with name '%s' is not in plot list of this plot drawer!" % plotname)
            
    def update(self):
        """Update this widget. Along with regular tkinter update, redraws grid and plot."""
        self._drawGrid()    # redraw grid
        self._drawPoints()  # redraw points
        self._scaleLabel["text"] = "Scale: %1.1f" % self.scale
        super().update()    # tkinter's update
        
root = Tk()
pd = PlotDrawer(root)
pd.pack()
root.mainloop()