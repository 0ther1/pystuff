from tkinter import *

class Plot():
    """Class representing a plot."""
    def __init__(self, name="New Plot", color="#000000", points=[], showpoints=True, showlines=True):
        """Create a new plot.
        [name] - name of this plot
        [color] - color of this plot lines and points
        [points] - points of this plot in format [(x, y), ...]
        [show_points] - draw points or not
        [show_lines] - draw lines or not"""
        self.name = name
        self.color = color
        self._points = points
        self.show_points = showpoints
        self.show_lines = showlines
    
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
        
    def add_point(self, point):
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
        if ("width" in kw):                 # if width is given in kw
            W = kw["width"]                 # set given width
        if ("height" in kw):                # if height is given in kw
            H = kw["height"]                # set given height
        self._plots = plots                 # [INTERNAL] plot list
        self._scale = scale                 # [INTERNAL] grid and plot scale
        self._grid_color = gridcolor        # [INTERNAL] grid color
        self._center_color = centercolor    # [INTERNAL] grid center color
        self._canvas_w = W                  # [INTERNAL] width of canvas
        self._canvas_h = H                  # [INTERNAL] height of canvas
        self._draw_axis = False             # [INTERNAL] visibility of axis NOT USED
        self._center = [0, 0]               # [INTERNAL] center of plot (in plot axis) (x,y)
        self._screen_center = [W/2, H/2]    # [INTERNAL] center of plot (in screen axis) (x,y)
        self._steps = [0, 0]                # [INTERNAL] step of axis (x,y) NOT USED
        self._user_scaled = False           # [INTERNAL] set if user changed scale
        self._last_mouse_pos = []           # [INTERNAl] last mouse position
        self._plot_labels = []              # [INTERNAl] plot names and colors
        # Setup canvas
        bgcolor = "white"                   # background color of canvas
        if ("bg" in kw.keys()):             # if background color is given in kw
            bgcolor = kw["bg"]              # set given color
        self._canvas = Canvas(self, width=self._canvas_w, height=self._canvas_h, bg=bgcolor, highlightthickness=0)    # canvas for drawing
        self._canvas.grid(column=0, row=0, columnspan=20)       # place canvas 
        self._canvas.bind("<Motion>", self._show_cooridnates)    # bind on mouse movement for canvas 
        self._canvas.bind("<B1-Motion>", self._move_grid)        # bind on mouse drag for canvas
        self._canvas.bind("<MouseWheel>", self._change_scale)    # bind on mouse wheel for canvas
        self._canvas.bind("<Leave>", self._erase_coordinates)    # bind on mouse leave for canvas
        self._canvas.bind("<Button-1>", lambda e: self._last_mouse_pos.extend([e.x, e.y]))
        self._canvas.bind("<ButtonRelease-1>", lambda e: self._last_mouse_pos.clear())    # bind on mouse button 1 release - clear last mousce position
        self._info_label = Label(self, text="X: --.------ ; Y: --.------")   # label for displaying coordinates
        self._info_label.grid(column=0, row=2)                   # place label
        self._scale_label = Label(self, text="Scale: %1.1f" % self.scale)    # label for displaying current scale
        self._scale_label.grid(column=19, row=2)
        self._frm_plot_labels = Frame(self)                         # frame for plot name labels
        self._frm_plot_labels.grid(row=1, column=0, columnspan=20)
        self._draw_grid()                                        # begin drawing grid
        self._draw_points()                                      # begin drawing points
        self._update_plot_labels()
        
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
        
    def _change_scale(self, event):
        """[INTERNAL] handler for mouse wheel scaling."""
        if (not self._user_scaled):
            self._user_scaled = True
        try:
            self.scale += 0.5 if event.delta < 0 else -0.5  # try to change scale
        except ValueError:                                  # except invalid values 
            pass
        
    def _move_grid(self, event):
        """[INTERNAL] handler for mouse canvas movement."""
        if (not self._user_scaled):
            self._user_scaled = True
        self._screen_center[0] -= self._last_mouse_pos[0] - event.x
        self._screen_center[1] -= self._last_mouse_pos[1] - event.y
        self._last_mouse_pos = [event.x, event.y]
        self.update()
        
    def _show_cooridnates(self, event):
        """[INTERNAL] handler for displaying coordinates under pointer."""
        co = self._from_screen_coordinates([event.x, event.y])                # convert pointer coordinates to plot axis
        for plot in self._plots:                                            # for every plot
            for p in plot.points:                                           # for every point
                if (abs(p[0] - co[0]) < 0.1 and abs(p[1] - co[1]) < 0.1):   # if pointer is near point
                    co = p                                                  # snap to this point
                    break
        self._info_label["text"] = "X: %.06f ; Y: %.06f" % (co[0], co[1])   # display coordinates
        
    def _update_plot_labels(self):
        """[INTERNAL] update labels with plot names."""
        for lbl in self._frm_plot_labels.children:
            lbl.destroy()
        for plt in self._plots:
            lbl = Label(self._frm_plot_labels, text="——— %s" % plt.name, fg=plt.color)
            lbl.pack()
        
    def _erase_coordinates(self, event):
        """[INTERNAL] handler for displaying defalut value when coordinates cannot be received."""
        self._info_label["text"] = "X: --.------ ; Y: --.------"

    def _from_screen_coordinates(self, point):
        """[INTERNAL] convert coordinates from screen to plot axis."""
        grid_count_h = (self.HORIZONTALS*self._scale)     # count of horizontals
        grid_count_v = (self.VERTICALS*self._scale)       # count of vertical
        grid_width = self._canvas_w / grid_count_h          # width of one cell in grid
        grid_height = self._canvas_h / grid_count_v         # height of one cell in grid
        screen_center = [self._screen_center[0] - self._center[0]*grid_width, self._screen_center[1] + self._center[1]*grid_height]  # center of plot in screen coordinates
        return [(point[0] - screen_center[0]) / grid_width, -(point[1] - screen_center[1]) / grid_height]   # return converted coordinates
        
    def _to_screen_coordinates(self, point):
        """[INTERNAL] convert coordinates from plot to screen axis."""
        grid_count_h = (self.HORIZONTALS*self._scale)     # count of horizontals
        grid_count_v = (self.VERTICALS*self._scale)       # count of vertical
        grid_width = self._canvas_w / grid_count_h          # width of one cell in grid
        grid_height = self._canvas_h / grid_count_v         # height of one cell in grid
        screen_center = [self._screen_center[0] - self._center[0]*grid_width, self._screen_center[1] + self._center[1]*grid_height] # center of plot in screen coordinates
        return [point[0]*grid_width + screen_center[0], screen_center[1] - point[1]*grid_height]    # return converted coordinates
        
    def _setup_grid(self):
        """[INTERNAL] prepare grid attributes."""
        X = []      # all x coordinates of all points
        Y = []      # all y coordinates of all points
        abs_x = []   # all absolute x coordinates of all points
        abs_y = []   # all absolute y coordinates of all points
        point_count = 0                      # count of all points
        for plot in self._plots:            # for every plot
            point_count += len(plot.points)
            for p in plot.points:           # for every point
                X.append(p[0])              # add x coordinate
                Y.append(p[1])              # add y coordinate
                abs_x.append(abs(p[0]))      # add absolute x coordinate
                abs_y.append(abs(p[1]))      # add absolute y coordinate
        if (point_count > 0):
            self._center = [sum(X)/point_count, sum(Y)/point_count]   # calculate center of plot
            self._steps = [sum(abs_x) / self.HORIZONTALS, sum(abs_y) / self.VERTICALS]    # calculate step of grid
        
    def _draw_grid(self):
        """[INTERNAL] draw grid on canvas."""
        self._setup_grid()                           # prepare grid attributes
        self._canvas.delete(ALL)                    # clear canvas
        multiplier = (self._scale - 10*(self.scale//10))
        if (multiplier < 1):
            multiplier = 1
        grid_count_h = int(self.HORIZONTALS*multiplier) # count of horizontals 
        grid_count_v = int(self.VERTICALS*multiplier)   # count of verticals        
        grid_width = self._canvas_w / grid_count_h      # width of one cell in grid
        grid_height = self._canvas_h / grid_count_v     # height of one cell in grid
        cntr = self._to_screen_coordinates([0, 0])    # get center (0, 0) in screen coordinates
        line_y = cntr[1]
        sign = 1
        while (True):
            if (sign == 1):
                if (line_y > self._canvas_h):
                    break
            else:
                if (line_y < 0):
                    break
            line_y += grid_height * sign
            if (0 <= line_y <= self._canvas_h):
                self._canvas.create_line(0, line_y, self._canvas_w, line_y, fill=self._grid_color)
        line_y = cntr[1]
        sign = -1
        while (True):
            if (sign == 1):
                if (line_y > self._canvas_h):
                    break
            else:
                if (line_y < 0):
                    break
            line_y += grid_height * sign
            if (0 <= line_y <= self._canvas_h):
                self._canvas.create_line(0, line_y, self._canvas_w, line_y, fill=self._grid_color)  
        line_x = cntr[0]
        sign = 1
        while (True):
            if (sign == 1):
                if (line_x > self._canvas_w):
                    break
            else:
                if (line_x < 0):
                    break
            line_x += grid_width * sign
            if (0 <= line_x <= self._canvas_w):
                self._canvas.create_line(line_x, 0, line_x, self._canvas_w, fill=self._grid_color)
        line_x = cntr[0]
        sign = -1
        while (True):
            if (sign == 1):
                if (line_x > self._canvas_w):
                    break
            else:
                if (line_x < 0):
                    break
            line_x += grid_width * sign
            if (0 <= line_x <= self._canvas_w):
                self._canvas.create_line(line_x, 0, line_x, self._canvas_w, fill=self._grid_color)          
        if (0 <= cntr[0] <= self._canvas_w):         # if x of center is within screen space - draw it
            self._canvas.create_line(cntr[0], 0, cntr[0], self._canvas_h, fill=self._center_color, width=2)
        if (0 <= cntr[1] <= self._canvas_h):         # if y of center is within screen space - draw it
            self._canvas.create_line(0, cntr[1],self._canvas_w, cntr[1], fill=self._center_color, width=2)  
            
    def _draw_points(self):
        """[INTERNAL] draw all points of plot."""
        point_size = 4 / self.scale# /((self.scale//10)+1)
        for plot in self._plots:
            last_point = None                        # previous point
            for p in plot.points:                   # for every point
                xy = self._to_screen_coordinates(p)   # convert point coordinates to screen space
                if (not self._user_scaled):
                    if (0 > xy[0] or xy[0] > self._canvas_w or 0 > xy[1] or xy[1] > self._canvas_h):  # if point outside screen space
                        try:
                            self.scale += 0.1           # try to increase scale
                        except ValueError:              # excepting maximum scale
                            pass
                        break
                if (plot.show_points):
                    self._canvas.create_oval(xy[0]-point_size//2, xy[1]-point_size//2, xy[0]+point_size//2, xy[1]+point_size//2, fill=plot.color, outline=plot.color) # draw point
                if (last_point):                     # if this is not first point of plot
                    xy2 = self._to_screen_coordinates(last_point)              # convert previous point coordinates to screen space
                    if (plot.show_lines):
                        self._canvas.create_line(xy[0], xy[1], xy2[0], xy2[1], fill=plot.color, width=1*((self.scale//10)+1))  # draw line between previous and current points
                last_point = p                       # set current point as prevoius            
            
    def add_plot(self, plot):
        """Add a new plot to draw. 'plot' - a Plot object"""
        if (isinstance(plot, Plot)):    # if it's a Plot
            self._plots.append(plot)    # add it
            self._update_plot_labels()
            self.update()               # update to redraw
        else:
            raise TypeError("'plot' must be a Plot object!")
        
    def add_point_to_plot(self, plotname, point):
        """Add new point to plot with name 'plotname'."""
        plot = None
        for plt in self._plots:
            if (plt.name == plotname):
                plot = plt
                break
        if (plot):
            plot.add_point(point)
            self.update()
        else:
            raise ValueError("Plot with name '%s' is not in plot list of this plot drawer!" % plotname)
            
    def update(self):
        """Update this widget. Along with regular tkinter update, redraws grid and plot."""
        self._draw_grid()    # redraw grid
        self._draw_points()  # redraw points
        self._scale_label["text"] = "Scale: %1.1f" % self.scale
        super().update()    # tkinter's update