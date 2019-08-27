#  ================================================================================================
#  ==  BRIEF  : checklist class and tools
#  ==  AUTHOR : stephen.burns.menary@cern.ch
#  ================================================================================================


import ipywidgets
from IPython.display import clear_output


#  CheckListButton class
#  - wrapper for ipywidgets.Button widget
#  - stores button colour and links to the parent (CheckListRow) to be called when clicked
#
class CheckListButton (ipywidgets.Button) :
    def __init__ (self, description="", parent=None, colour=None) :
        super(CheckListButton, self).__init__(description=description)
        self.parent = parent
        self.colour = colour
        self.on_click(self.on_button_click)
    def clear (self) :
        self.style.button_color = None
    def make (self) :
        return self  #ipywidgets.VBox([self, self.out])
    def on_button_click(self, b):
        previous_colour = self.style.button_color
        self.parent.clear_buttons()
        if previous_colour is None : self.style.button_color = self.colour
        else : self.style.button_color = None


#  CheckListRow class
#  - collection of five CheckListButton objects with description and message panels
#  - allows a button click to be propagated between button instances
#
class CheckListRow (ipywidgets.VBox) :
    def __init__ (self, description="", ljust=30) :
        self.buttons     = []
        self.description = description
        self.ljust       = ljust
        self.buttons.append(ipywidgets.Output())
        self.buttons.append(CheckListButton("Failed"      , self, "salmon"))
        self.buttons.append(CheckListButton("Attention"   , self, "navajowhite" ))
        self.buttons.append(CheckListButton("Untested"    , self, "lemonchiffon"))
        self.buttons.append(CheckListButton("Not required", self, "palegreen"))
        self.buttons.append(CheckListButton("Passed"      , self, "lime"     ))
        buttons = ipywidgets.HBox(self.buttons)
        self.message_out = ipywidgets.Output()
        super(CheckListRow, self).__init__([buttons, self.message_out])
        with self.buttons[0] :
            print("\u2022  " + self.description.ljust(self.ljust))
        self.untested()
    def failed (self, comment=None) :
        self.buttons[1].click()
        if comment is not None :
            self.comment(comment)
    def attention (self, comment=None) :
        self.buttons[2].click()
        if comment is not None :
            self.comment(comment)
    def untested (self, comment=None) :
        self.buttons[3].click()
        if comment is not None :
            self.comment(comment)
    def not_required (self, comment=None) :
        self.buttons[4].click()
        if comment is not None :
            self.comment(comment)
    def passed (self, comment=None) :
        self.buttons[5].click()
        if comment is not None :
            self.comment(comment)
    def clear_buttons (self) :
        for button in self.buttons :
            if type(button) is not CheckListButton : continue
            button.clear()
    def comment (self, message) :
        with self.message_out :
            clear_output()
            print(" "*(3+self.ljust) + message)


#  CheckList class
#  - collection of CheckListRows
#  - rows can be indexed according to their given description
#
class CheckList (ipywidgets.VBox) :
    def __init__ (self, *argv, **kwargs) :
        self.rows = []
        for arg in argv :
            self.rows.append(CheckListRow(arg))
        for table_num in range(1, 1+kwargs.get("num_tables", 0)) :
        	self.rows.append(CheckListRow(f"Table {table_num}: central values"))
        super(CheckList, self).__init__(self.rows)
    def __getitem__ (self, key) :
        if type(key) is int :
            if key >= self.rows :
                raise IndexError(f"Index {key} is out of range ({len(self)})")
            return self.rows[key]
        if type(key) is str :
            for row in self.rows :
                if row.description != key : continue
                return row
        raise KeyError(f"Key {key} not in CheckList")
    def __len__ (self) :
        return len(self.rows)
     