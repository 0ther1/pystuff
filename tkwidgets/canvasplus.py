from tkinter import *

class CanvasPlus(Canvas):
    """Scalable and movable canvas."""
    def __init__(self, master=None, scale: float=1.0, minscale: float=1.0, maxscale: float=10.0, scalestep: float=1.0, allowscale=True, allowmove=True, **kw):
        """Create a new CanvasPlus ojbect.
        scale - current scale;
        minscale - minimum scale;
        maxscale - maximum scale;
        scalestep - scale step value."""
        super().__init__(master, kw)
        self._scale = scale
        self._scale_min = minscale
        self._scale_max = maxscale
        self._scale_step = scalestep
        self._scale_old = self._scale
        self._scale_point = [0, 0]
        self._transformable = False
        self.allow_move = allowmove
        self.allow_scale = allowscale        
        self.bind("<MouseWheel>", self._on_scroll)
        self.bind("<Button-1>", self._on_rmb)
        self.bind("<ButtonRelease-1>", self._on_rmb_release)
        self.bind("<B1-Motion>", self._on_drag)
        
    @property
    def scale(self):
        return self._scale
        
    @scale.setter
    def scale(self, value): 
        """Get/set scale. Value must be in range [scale_min, scale_max]."""
        if (not (self._transformable and self.allow_scale)):
            return
        if (value >= self._scale_min and value <= self._scale_max): 
            if (value != self._scale): 
                self._scale = value
                self.update() 
        else:
            raise ValueError("Scale must be in range [%.1f, %.1f]!" % (self._scale_min, self._scale_max))
        
    def _on_scroll(self, event):
        self._scale_point = [event.x, event.y]
        if (event.delta > 0):
            self.scale_up()
        else:
            self.scale_down()
        self._scale_point = [0, 0]
        
    def _on_rmb(self, event):
        if (self._transformable and self.allow_move):
            self.configure(cursor="hand2")
            self.scan_mark(event.x, event.y)
            
    def _on_rmb_release(self, event):
        self.configure(cursor="arrow")
        
    def _on_drag(self, event):
        if (self._transformable and self.allow_move):
            self.scan_dragto(event.x, event.y, 1)
            
    def _create(self, itemType, args, kw):
        self._transformable = True
        return super()._create(itemType, args, kw)            
        
    def scale_up(self):
        """Scale up one step."""
        if (self._scale + self._scale_step > self._scale_max):
            self.scale = self._scale_max
        else:
            self.scale += self._scale_step
        
    def scale_down(self):
        """Scale down one step."""
        if (self._scale - self._scale_step < self._scale_min):
            self.scale = self._scale_min
        else:
            self.scale -= self._scale_step
            
    def delete(self, *args):
        self._transformable = bool(self.find_all())
        super().delete(args)
            
    def update(self):
        """Update this widget. Also rescales items."""
        if (self._scale_old != self._scale):
            delta = (self._scale / self._scale_old)
            super().scale(ALL, *self._scale_point, delta, delta)
            self.configure(scrollregion = self.bbox("all"))
            self._scale_old = self._scale
        super().update()