from tkinter import *

class Table(Frame):
    """Table widget"""
    def __init__(self, master, rows=1, columns=1, cellwidth=10, displaylabels=[True, True], rowlabels=[], columnlabels=[], state="normal", **kw):
        """Creates a new table. Options:\n
        master : widget - parent of this widget;\n
        [rows] : integer - row count;\n
        [columns] : integer - column count;\n
        [cellwidth] : integer - width of one cell;\n
        [displaylabels] : bool - display or not table labels;\n
        [rowlabels] : list of strings - values of row labels;\n
        [columnlabels] : list of strings - values of column labels;\n
        [state] : string - state of cells, 'normal' or 'readonly';\n
        [kw] : dict - other tkinter options;
        """
        super().__init__(master, **kw)        # init base class
        self._matrix = []                     # [INTERNAL] table model
        self._row_labels = []                 # [INTERNAL] list of Label objects of rows
        self._col_labels = []                 # [INTERNAL] list of Label objects of columns
        self._row_labels_text = []            # [INTERNAL] list of values of row labels
        self._col_labels_text = []            # [INTERNAL] list of values of column labels
        self._rows = 0                        # [INTERNAL] count of rows in table
        self._columns = 0                     # [INTERNAL] count of columns in table
        self._cell_width = cellwidth          # [INTERNAL] width of one cell
        self._display_labels = [False, False] # [INTERNAL] are table labels visible
        self._state = "normal"                # [INTERNAL] state of cells (normal or readonly)
        self.rows = rows                      # set row count
        self.columns = columns                # set column count
        self.row_labels = rowlabels           # set row labels values
        self.column_labels = columnlabels     # set column label values
        self.display_labels = displaylabels   # set visibility of labels
        self.state = state                    # set state of cells
        self["bd"] = 2
    
    @property
    def rows(self):         # rows property
        return self._rows   # return row count
        
    @rows.setter
    def rows(self, value):  # rows property setter
        """Get/set row count. For setting row amount must be above zero."""
        if (value > 0):                                     # if value above zero
            if (value > self._rows):                        # if new value is greater than current row count
                self.add_rows(value-self._rows)              # add new rows
            elif (value < self._rows):                      # if lesser
                self.remove_rows(range(value, self._rows))   # remove rows
        else:
            raise ValueError("Row count must be above zero!")
            
    @property
    def columns(self):          # columns property
        return self._columns    # return column count
        
    @columns.setter
    def columns(self, value):   # columns property setter
        """Get/set column count. For setting column amount must be above zero."""
        if (value > 0):                                         # if value above zero
            if (value > self._columns):                         # if new value is greater than current column count
                self.add_columns(value-self._columns)            # add new columns
            elif (value < self._columns):                       # if lesser
                self.remove_columns(range(value, self._columns)) # remove columns
        else:
            raise ValueError("Column count must be above zero!")
            
    @property
    def row_labels(self):                    # row labels values setter
        return self._row_labels_text.copy()   # return copy of values
        
    @row_labels.setter
    def row_labels(self, value):             # row lables values property setter
        """Get/set rows' labels values. Must be list or tuple of strings. List/tuple length must not be lesser than row count."""
        if (isinstance(value, list) or isinstance(value, tuple)):   # if value type is list/tuple
            if (len(value) < self.rows):                            # if length of value is lesser than row count
                if (len(value) != 0):                               # and there is rows, raise exception
                    raise ValueError("Row labels count cannot be less than row count!")
            else:                                                   # else 
                self._row_labels_text = list(value)                   # set row labels values
                self._update_labels()                                # update all labels to apply changes
        else:
            raise TypeError("Value for row labels must be list or tuple!")
            
    @property
    def column_labels(self):                 # column labels values setter
        return self._col_labels_text.copy()   # return copy of values
        
    @column_labels.setter
    def column_labels(self, value):          # column lables values property setter
        """Get/set columns' labels values. Must be list or tuple of strings. List/tuple length must not be lesser than column count."""
        if (isinstance(value, list) or isinstance(value, tuple)):   # if value type is list/tuple
            if (len(value) < self.columns):                         # if length of value is lesser than column count
                if (len(value) != 0):                               # and there is columns, raise exception
                    raise ValueError("Column labels count cannot be less than column count!")
            else:                                                   # else 
                self._col_labels_text = list(value)                   # set column labels values
                self._update_labels()                                # update all labels to apply changes
        else:
            raise TypeError("Value for column labels must be list or tuple!")
            
    @property
    def display_labels(self):                # visibility of labels property
        return self._display_labels.copy()   # return visibility state
        
    @display_labels.setter
    def display_labels(self, value):         # visibility of labels property setter
        """Get/set visibility of labels. Must be list/tuple of two bools : first - visibility of rows, second - columns."""
        if (isinstance(value, list) or isinstance(value, tuple)):   # if value is valid
            if (self._display_labels != value):                      # if value is not current state    
                self._display_labels = value                         # change state
                self._update_labels()                                # update labels to apply changes
        else:
            raise TypeError("Value for label visibility must be list or tuple!")
            
    @property
    def state(self):        # state of cells property
        return self._state  # return state
        
    @state.setter
    def state(self, value):                             # state of cells property setter
        """Get/set state of cells. Must be 'normal' or 'readonly.'"""
        if (value == "normal" or value == "readonly"):  # if value is valid
            if (self._state != value):                  # and not equals current state
                self._state = value                     # change state
                for line in self._matrix:               # for line in matrix
                    for e in line:                      # for entry in line
                        e["state"] = value              # change state
            
        else:
            raise ValueError("Table state can only be 'normal' or 'readonly'")
            
    def add_columns(self, amount):
        """Append empty `amount` columns."""
        if (amount <= 0):                                       # if amount is non-positive raise exception
            raise ValueError("Adding column amount must be above zero!")
        for k in range(amount):                                 # for every new column
            for i, row in enumerate(self._matrix):              # for every row in model
                new_cell = Entry(self, width=self._cell_width, bd=1) # create new cell
                row.append(new_cell)                             # append it to row
                new_cell.grid(row=i+1, column=self.columns+1)    # place it on widget
            self._columns += 1                                  # increase column count
            if (self.columns > len(self.column_labels)):         # if column count is greater than label values count
                self._col_labels_text.append(str(self.columns))   # append column position as new label value
        self._update_labels()                                    # update labels to apply changes
                
    def add_rows(self, amount):
        """Append empty `amount` rows."""
        if (amount <= 0):                                       # if amount is non-positive raise exception
            raise ValueError("Adding rows amount must be above zero!")
        if (self._columns == 0):                                # if there is no columns (table is empty on init)
            self.columns = 1                                    # append one column
        for k in range(amount):                                 # for every new row
            new_row = []                                         # new row
            for j in range(self.columns):                       # for column count
                new_cell = Entry(self, width=self._cell_width, bd=1) # create new cell
                new_row.append(new_cell)                          # insert it in new row
                new_cell.grid(row=self.rows+1, column=j+1)       # place it on widget
            self._matrix.append(new_row)                         # insert new row in model
            self._rows += 1                                     # increase row count
            if (self.rows > len(self.row_labels)):               # if row count is greater than label values count
                self._row_labels_text.append(str(self.rows))      # append row position as new label value
        self._update_labels()                                    # update labels to apply changes
            
    def remove_rows(self, indices):
        """Remove rows at `indices`. Must be list or tuple of indices"""
        if (not (isinstance(indices, list) or isinstance(indices, tuple))):
            raise TypeError("Indices must be a list or a tuple of integers!")
        for i in indices:                                       # verify indices
            if (i < 0 or i >= self.rows):
                raise ValueError("Row index out of range!")
        removed = []                                            # list of already removed indices in one call
        offset = 0                                              # offset (when cells pops out of list next ones shifting)
        for i in indices:
            idx = i
            for r in removed:                                   # check already removed indices
                if (idx > r):                                   # if current index is after removed ones
                    idx -= offset                               # add offset
                    break
            if (idx != self.rows - 1):
                for j in range(idx+1, self.rows):               # for every next row
                    for k in range(self.columns):               # for every cell
                        self._matrix[j][k].grid_configure(row=j)# shift position on widget
            delRow = self._matrix.pop(idx)                      # pop and save row
            removed.append(idx)                                 # remember deleted index
            offset += 1                                         # increase offset
            for c in delRow:                                    # for cell in row to delete
                c.destroy()                                     # delete cell
            self._rows -= 1                                     # decrease row count
        self._update_labels()                                    # update labels to apply changes
    
    def remove_columns(self, indices):
        """Remove columns at `indices`. Must be list or tuple of indices"""
        if (not (isinstance(indices, list) or isinstance(indices, tuple))):
            raise TypeError("Indices must be a list or a tuple of integers!")        
        for i in indices:                                       # verify indices
            if (i < 0 or i >= self.columns):
                raise ValueError("Column index out of range!")
        removed = []                                            # list of already removed indices in one call
        offset = 0                                              # offset (when cells pops out of list next ones shifting)
        for i in indices:
            idx = i
            for r in removed:                                   # check already removed indices
                if (idx > r):                                   # if current index is after removed ones
                    idx -= offset                               # add offset
                    break        
            for row in self._matrix:                            # for every row
                if (idx != self.columns - 1):
                    for j in range(idx+1, self.columns):        # for every next cell
                        row[j].grid_configure(column=j)         # shift position on widget
                cell = row.pop(idx)                             # pop and save column
                cell.destroy()                                  # delete cell
            self._columns -= 1                                  # decrease column count
            removed.append(idx)                                 # remember deleted index
            offset += 1                                         # increase offset
        self._update_labels()                                    # update labels to apply changes
            
    def get(self, row, column):
        """Get item at row and column."""
        if ((row < 0 or row >= self.rows) or (column < 0 or column >= self.columns)):   # verify index
            raise ValueError("Index out of range!")
        return self._matrix[row][column].get()                                          # return item
        
    def set(self, value, row, column):
        """Set item at row and column."""
        if ((row < 0 or row >= self.rows) or (column < 0 or column >= self.columns)):   # verify index
            raise ValueError("Index out of range!")
        etr = self._matrix[row][column]                                                 # get entry
        etr.delete(0, END)                                                              # clear entry contents
        etr.insert(END, str(value))                                                     # set new entry contents
        
    def _update_labels(self):
        """[INTERNTAL] Update label count or/and it's contents."""
        if (self._display_labels[0]):                                      # if row labels are visible
            if (len(self._row_labels) > self.rows):                        # if rows labels values count is greater than row count
                to_delete = []                                             # list of labels to delete
                for i in range(self.rows, len(self._row_labels)):          # for every label to delete
                    to_delete.append(self._row_labels[i])                   # save it for later
                for l in to_delete:                                        # for every label
                    lbl = self._row_labels.pop(self._row_labels.index(l))   # pop from list
                    lbl.destroy()                                         # delete it
            elif (len(self._row_labels) < self.rows):                      # else if row labels values count is lesser than row count
                for i in range(self.rows - len(self._row_labels)):         # for amount of labels to add
                    self._row_labels.append(Label(self))                   # add new label
        if (self._display_labels[1]):                                      # if column labels are visible
            if (len(self._col_labels) > self.columns):                     # if column labels values count is greater than column count
                to_delete = []                                             # list of labels to delete
                for i in range(self.columns, len(self._col_labels)):       # for every label to delete
                    to_delete.append(self._col_labels[i])                   # save it for later
                for l in to_delete:                                        # for every label
                    lbl = self._col_labels.pop(self._col_labels.index(l))   # pop from list
                    lbl.destroy()                                         # delete it
            elif (len(self._col_labels) < self.columns):                   # else if column labels values count is lesser than column count
                for i in range(self.columns - len(self._col_labels)):      # for amount of labels to add
                    self._col_labels.append(Label(self))                   # add new label
        if (self._display_labels[0]):                                      # if row labels are visible
            for i, lbl in enumerate(self._row_labels):                     # for every row label
                lbl["bg"] = "#AAAAAA" if i % 2 == 0 else "#CCCCCC"        # set diffirent colors for odd and even labels
                lbl["text"] = self.row_labels[i]                           # set label text
                lbl["bd"] = 1
                lbl.grid(row=i+1, column=0, sticky="ns")                  # place label in widget
        if (self._display_labels[1]):                                      # if column labels are visible
            for i, lbl in enumerate(self._col_labels):                     # for every column label
                lbl["bg"] = "#AAAAAA" if i % 2 == 0 else "#CCCCCC"        # set diffirent colors for odd and even labels
                lbl["text"] = self.column_labels[i]                        # set label text
                lbl["bd"] = 1
                lbl.grid(row=0, column=i+1, sticky="we")                  # place label in widget