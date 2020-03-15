from vector import Vector
from matrix import Matrix

class Place:
    """A place in Petri net.
    `name`: str - name of this place;
    `tokens`: int - amount of tokens in this place."""
    def __init__(self, name: str, tokens: int=0):
        """Create a new Place object.
        `name` - name;
        [tokens] - amount of tokens."""
        self.name = name
        self.tokens = tokens
        
class Transition:
    """A transition in Petri net.
    `name`: str - name of this transition;
    `inputs`: list - copy of all input places for this transition;
    `outputs`: list - copy of all output places for this transition.
    Both `inputs` and `outputs` structures are: list of lists [p, a] where p - Place object, a - number of arcs."""
    def __init__(self, name: str):
        """Create a new Transition object.
        `name` - name."""
        self.name = name
        self._inputs = []
        self._outputs = []
        
    @property
    def inputs(self) -> list:
        """Get copy of all input places."""
        return self._inputs.copy()
    
    @property
    def outputs(self) -> list:
        """Get copy of all output places."""
        return self._outputs.copy()
        
    def find(self, name: str, out: bool=False) -> Place:
        """Get first occurence of place with given name.
        `name` - name of place to find;
        [out] - True - find in output places, False - in input places.
        Raises ValueError if place is not found."""
        lst = self._outputs if out else self._inputs
        for p in lst:
            if (p.name == name):
                return p
        raise ValueError("Place '%s' is not in %s." % (name, "outputs" if out else "inputs"))
        
    def exec(self):
        """Execute this transition. Raises RuntimeError if transition is not enabled."""
        if (not self.enabled()):    
            raise RuntimeError("Transition cannot be started: one of input places ('%s') has not enough tokens." % p[0].name)
        for p in self._inputs:
            p[0].tokens -= p[1]
        for p in self._outputs:
            p[0].tokens += p[1]
            
    def enabled(self) -> bool:
        """Check if this transition is enabled (all input places has token amount >= arc count)."""
        for p in self._inputs:
            if (p[0].tokens < p[1]):
                return False
        return True
        
    def connect(self, place: Place, arcs: int, out: bool=False):
        """Connect given place to this transition with given arc count.
        `place` - Place object to connect;
        `arcs` - amount of arcs to connect (> 0);
        [out] - True - connect as output place, False - as input place."""
        if (arcs < 1):
            raise ValueError("`arcs` must be int > 0.")
        lst = self._outputs if out else self._inputs
        for p in lst:
            if (place == p):
                p[1] += arcs
                break
        else:
            lst.append( [place, arcs] )
            lst.sort(key=lambda io: io[0].name)
            
    def disconnect(self, place: Place, arcs: int=-1, out: bool=False):
        """Disconnect given place from this transition with given arc count.
        `place` - Place object to disconnect;
        `arcs` - amount of arcs to disconnect (> 0), -1 - disconnect all arcs;
        [out] - True - disconnect as output place, False - as input place."""        
        if (arcs > 0 or arcs == -1):
            raise ValueError("`arcs` must be int > 0, or -1.")
        lst = self._outputs if out else self._inputs
        for p in lst:
            if (place in p):
                if (arcs != -1):
                    if (p[1] - arcs < 0):
                        raise ValueError("`arcs` must be <= place arc count.")
                    p[1] -= arcs
                else:
                    p[1] = 0
                if (p[1] == 0):
                    lst.remove(p)
                break
        else:
            raise ValueError("Given place '%s' is not connected to this transition." % place.name)
        
class PetriNet:
    """A Petri net.
    `places`: list - copy of all places in this net;
    `transitions`: list - copy of all transitions in this net.
    Both lists sorted by places and transition names."""
    def __init__(self, placecount: int=0, transcount: int=0, inputs: list=[], outputs: list=[]):
        """Create a new PetriNet object.
        [placecount] - amount of places to create with names p0, p1, ...;
        [transcount] - amount of transitions to create with names t0, t1, ...;
        [inputs] - list of input places to connect to each transition in format [t1, t2, ...] where t* = [p1, p2, ...] where p* - Place object or name of place in this net;
        [outputs] - list of output places to connect to each transition in format [t1, t2, ...] where t* = [p1, p2, ...] where p* - Place object or name of place in this net.
        
        E.g PetriNet(2, 3, [ ["p0"], [], ["p1"] ], [ [], ["p1"], ["p0"] ])."""
        self._places = [Place("p%d" % i) for i in range(placecount)]
        self._transitions = [Transition("t%d" % i) for i in range(transcount)]
        if (inputs):
            if (self._transitions and self._places):
                for i, inp in enumerate(inputs):
                    for p in inp:
                        if (isinstance(p, str)):
                            self.connect(self.find_place(p), self._transitions[i], 1)
                        else:
                            raise TypeError("`inputs` must be a list/tuple of lists/tuples for every transition of ints/strings of indices/names of places in this net.")
        if (outputs):
            if (self._transitions and self._places):
                for i, out in enumerate(outputs):
                    for p in out:
                        if (isinstance(p, str)):
                            self.connect(self.find_place(p), self._transitions[i], 1, True)
                        else:
                            raise TypeError("`outputs` must be a list/tuple of lists/tuples for every transition of ints/strings of indices/names of places in this net.")                        
         
    @property
    def places(self) -> list:
        """Get copy of all places in this net."""
        return self._places.copy()
    
    @property
    def transitions(self) -> list:
        """Get copy of all transitions in this net."""
        return self._transitions.copy()
        
    def __contains__(self, object):
        if (isinstance(object, Place)):
            return object in self._places
        elif (isinstance(object, Transition)):
            return object in self._transitions
        else:
            raise TypeError("`object` must be a Place or Transition object.")
        
    def find_place(self, name: str) -> Place:
        """Get first occurence of place with given name. Raises ValueError if place is not found."""
        for p in self._places:
            if (p.name == name):
                return p
        raise ValueError("Place '%s' is not in net." % name)
    
    def find_transition(self, name: str) -> Transition:
        """Get first occurence of transition with given name. Raises ValueError if transition is not found."""
        for t in self._transitions:
            if (t.name == name):
                return t
        raise ValueError("Transition '%s' is not in net." % name)
    
    def add_place(self, place: Place, autoname=True) -> str:
        """Add place to this net and return it's name. Raises ValueError if given place already in this net.
        [autoname] - give this place name 'p*' where * lowest available index."""
        if (place in self._places):
            raise ValueError("Given place '%s' is already in net." % place.name)
        if (autoname):
            i = 0
            while (True):
                try:
                    self.find_place("p%d" % i)
                except ValueError:
                    break
                i += 1
            place.name = "p%d" % i
        self._places.append(place)
        self._places.sort(key=lambda p: p.name)
        return place.name
        
    def remove_place(self, place: [Place, str]) -> Place:
        """Remove place from this net and return it. Raises ValueError if given place is not in this net."""
        if (isinstance(place, str)):
            place = self.find_place(place)
        elif (not isinstance(place, Place)):
            raise TypeError("`place` must be a Place object or string name of place in this net.")
        if (place not in self._places):
            raise ValueError("Given place '%s' is not in net." % place.name)
        self._places.remove(place)
        for t in self._transitions:
            t._inputs = list(filter(lambda l: l[0] != place, t._inputs))
            t._outputs = list(filter(lambda l: l[0] != place, t._outputs))
        return place
        
    def add_transition(self, transition: Transition, autoname=True) -> str:
        """Add transition to this net and returns it's name. Raises ValueError if given transition already in this net.
        [autoname] - give this transition name 't*' where * lowest available index."""
        if (transition in self._transitions):
            raise ValueError("Given transition '%s' is already in net." % transition.name)
        if (autoname):
            i = 0
            while (True):
                try:
                    self.find_transition("t%d" % i)
                except ValueError:
                    break
                i += 1
            transition.name = "t%d" % i        
        self._transitions.append(transition)
        self._transitions.sort(key=lambda t: t.name)
        return transition.name
        
    def remove_transition(self, transition: [Transition, str]) -> Transition:
        """Remove transition from this net and return it. Raises ValueError if given transition is not in this net."""
        if (isinstance(transition, str)):
            transition = self.find_transition(transition)
        elif (not isinstance(transition, Transition)):
            raise TypeError("`transition` must be a Transition object or string name of transition in this net.")        
        if (transition not in self._transitions):
            raise ValueError("Given transition '%s' is not in net." % transition.name)
        self._transitions.remove(transition)
        return transition
        
    def exec(self, transitions: list):
        """Execute this network in given order.
        `transitions` - sequence of Transition object or their names to execute."""
        transitions = transitions.copy()
        for i, t in enumerate(transitions):
            if (isinstance(t, str)):
                t = self.find_transition(t)
                transitions[i] = t
            if (isinstance(t, Transition)):                
                if (t not in self._transitions):
                    raise ValueError("Given transition '%s' is not in net." % t.name)
            else:
                raise TypeError("`transitions` must be a list of Transition objects or string names of transitions in this net.")
        for t in transitions:
            try:
                t.exec()
            except RuntimeError:
                raise
            
    def inputs(self, object: [Place, Transition, str]) -> list:
        """Get input places for transition or input transitions for place."""
        result = []
        if (isinstance(object, str)):
            try:
                object = self.find_place(object)
            except ValueError:
                try:
                    object = self.find_transition(object)
                except ValueError:
                    raise ValueError("Could not found place or transition with name '%s'." % object)
        if (isinstance(object, Place)):
            if (object not in self._places):
                raise ValueError("Given place '%s' is not in net." % object.name)
            for t in self._transitions:
                for o in t._outputs:
                    if (o[0] == object):
                        result += [t for i in range(o[1])]
                        break
        elif (isinstance(object, Transition)):
            if (object not in self._transitions):
                raise ValueError("Given transition '%s' is not in net." % object.name)
            for i in object._inputs:
                result += [i[0] for j in range(i[1])]
        return result
    
    def outputs(self, object: [Place, Transition, str]) -> list:
        """Get output places for transition or output transitions for place."""
        result = []
        if (isinstance(object, str)):
            try:
                object = self.find_place(object)
            except ValueError:
                try:
                    object = self.find_transition(object)
                except ValueError:
                    raise ValueError("Could not found place or transition with name '%s'." % object)        
        if (isinstance(object, Place)):
            if (object not in self._places):
                raise ValueError("Given place '%s' is not in net." % object.name)
            for t in self._transitions:
                for i in t._inputs:
                    if (i[0] == object):
                        result += [t for j in range(i[1])]
                        break
        elif (isinstance(object, Transition)):
            if (object not in self._transitions):
                raise ValueError("Given transition '%s' is not in net." % object.name)
            for o in object._outputs:
                result += [o[0] for i in range(o[1])]
        return result
    
    def input_arc_count(self, place: [Place, str], transition: [Transition, str]) -> int:
        """Get arc count from given input place to given transition."""
        if (isinstance(place, str)):
            try:
                place = self.find_place(place)
            except ValueError:
                raise 
        elif (not isinstance(place, Place)):
            raise TypeError("`place` must be a Place object or string name of place in this net.")
        if (isinstance(transition, str)):
            try:
                transition = self.find_transition(transition)
            except ValueError:
                raise             
        elif (not isinstance(transition, Transition)):
            raise TypeError("`transition` must be a Transition object or string name of transition in this net.")      
        for i in transition._inputs:
            if (i[0] == place):
                return i[1]
        return 0
            
    def output_arc_count(self, place: [Place, str], transition: [Place, str]) -> int:
        """Get arc count from given transition to given output place."""
        if (isinstance(place, str)):
            try:
                place = self.find_place(place)
            except ValueError:
                raise 
        elif (not isinstance(place, Place)):
            raise TypeError("`place` must be a Place object or string name of place in this net.")
        if (isinstance(transition, str)):
            try:
                transition = self.find_transition(transition)
            except ValueError:
                raise             
        elif (not isinstance(transition, Transition)):
            raise TypeError("`transition` must be a Transition object or string name of transition in this net.")        
        for o in transition._outputs:
            if (o[0] == place):
                return o[1]
        return 0
            
    def invert(self):
        """Invert this net (swap inputs and outputs)."""
        for t in self._transitions:
            t._inputs, t._outputs = t._outputs, t._inputs
            
    def duple(self):
        """Duple this net (swap places and transitions)."""
        new_places = []
        new_transitions = []
        create_places = True
        for i in range(len(self._places)):
            t = Transition("t%d" % i)
            for j in range(len(self._transitions)):
                if (create_places):
                    new_places.append(Place("p%d" % j))
                inputs = self.input_arc_count(self._places[i], self._transitions[j])
                if (inputs):
                    t.connect(new_places[j], inputs, True)
                outputs = self.output_arc_count(self._places[i], self._transitions[j])
                if (outputs):
                    t.connect(new_places[j], outputs)
            create_places = False
            new_transitions.append(t)
        self._places = new_places
        self._transitions = new_transitions
        
    def connect(self, place: [Place, str], transition: [Transition, str], arcs: int, out: bool=False):
        """Connect given place to given transition with given arc count.
        [out] - True - connect as output place, False - as input."""
        if (isinstance(place, str)):
            try:
                place = self.find_place(place)
            except ValueError:
                raise 
        elif (not isinstance(place, Place)):
            raise TypeError("`place` must be a Place object or string name of place in this net.")
        if (isinstance(transition, str)):
            try:
                transition = self.find_transition(transition)
            except ValueError:
                raise             
        elif (not isinstance(transition, Transition)):
            raise TypeError("`transition` must be a Transition object or string name of transition in this net.")        
        if (place in self._places):
            if (transition in self._transitions):
                transition.connect(place, arcs, out)
            else:
                raise ValueError("Transition '%s' is not in net." % transition.name)
        else:
            raise ValueError("Place '%s' is not in net." % place.name)
        
    def disconnect(self, place: [Place, str], transition: [Transition, str], arcs: int, out: bool=False):
        """Disconnect given place to given transition with given arc count.
        If `arcs` is -1 - disconnect all arcs.
        [out] - True - disconnect as output place, False - as input."""        
        if (isinstance(place, str)):
            try:
                place = self.find_place(place)
            except ValueError:
                raise 
        elif (not isinstance(place, Place)):
            raise TypeError("`place` must be a Place object or string name of place in this net.")
        if (isinstance(transition, str)):
            try:
                transition = self.find_transition(transition)
            except ValueError:
                raise             
        elif (not isinstance(transition, Transition)):
            raise TypeError("`transition` must be a Transition object or string name of transition in this net.")           
        if (place in self._places):
            if (transition in self._transitions):
                transition.disconnect(place, arcs, out)
            else:
                raise ValueError("Transition '%s' is not in net." % transition.name)
        else:
            raise ValueError("Place '%s' is not in net." % place.name)
        
    def marking(self, transitions: list=[]) -> list:
        """Get marking.
        [transitions] - sequence of Transition objects or their names - if given, calculates marking after executing this sequence.
        
        Warning! Does not considering order of execution and availability of transitions."""
        if (transitions):
            count = []
            if (isinstance(transitions[0], Transition)):
                for t in self._transitions:
                    count.append(transitions.count(t))
            elif (isinstance(transitions[0], str)):
                for t in self._transitions:
                    count.append(transitions.count(t.name))
            else:
                raise TypeError("`transitions` must be a list/tuple of Transition object or string names of transitions in this net.")
            sig = Vector(count)
            return self.incidence() * sig + Vector([p.tokens for p in self._places])
        return [p.tokens for p in self._places]
    
    def set_tokens(self, place: [Place, str], tokens: int):
        """Set tokens for given place."""
        if (isinstance(place, str)):
            try:
                place = self.find_place(place)
            except ValueError:
                raise
        if (isinstance(place, Place)):            
            try:
                self._places[self._places.index(place)].tokens = tokens
            except ValueError:
                raise ValueError("Place '%s' is not in net." % place.name)
        else:
            raise TypeError("`place` must be Place object or string name of place in this net.")
        
    def set_marking(self, marking: list):
        """Set marking (tokens for every place)."""
        if (isinstance(marking, (list, tuple))):            
            if (len(marking) != len(self._places)):
                raise ValueError("Length of `marking` must be same as places count in this net.")
            for i, p in enumerate(self._places):
                p.tokens = int(marking[i])
        else:
            raise TypeError("`marking` must be a list/tuple of ints.")
                
    def incidence(self):
        """Get incidence matrix of this net."""
        mat = Matrix(len(self._transitions), len(self._places))
        for i, t in enumerate(self._transitions):
            for j, p in enumerate(self._places):
                mat[i][j] = -self.input_arc_count(p, t) + self.output_arc_count(p, t)
        return mat
    
    def clear(self):
        """Clear this net."""
        self._places.clear()
        self._transitions.clear()
    
    def write(self, filepath: str):
        """Write net data to file."""
        with open(filepath, "wb") as file:
            file.write(int.to_bytes(len(self._places), 2, "little"))
            for p in self._places:
                file.write(p.name.encode() + b"\x00")
                file.write(int.to_bytes(p.tokens, 2, "little"))
            file.write(int.to_bytes(len(self._transitions), 2, "little"))
            for t in self._transitions:
                file.write(t.name.encode() + b"\x00")
                file.write(int.to_bytes(len(t.inputs), 2, "little"))
                for i in t.inputs:
                    file.write(int.to_bytes(self._places.index(i[0]), 2, "little"))
                    file.write(int.to_bytes(i[1], 2, "little"))
                file.write(int.to_bytes(len(t.outputs), 2, "little"))
                for o in t.outputs:
                    file.write(int.to_bytes(self._places.index(o[0]), 2, "little"))
                    file.write(int.to_bytes(o[1], 2, "little"))
                    
    def read(self, filepath: str):
        """Read net data from file."""
        self.clear()
        with open(filepath, "rb") as file:
            place_count = int.from_bytes(file.read(2), "little")
            for i in range(place_count):
                name = ""
                while (True):
                    char = file.read(1)
                    if (char == b"\x00"):
                        break
                    name += char.decode()
                tokens = int.from_bytes(file.read(2), "little")
                self.add_place(Place(name, tokens))
            trans_count = int.from_bytes(file.read(2), "little")
            for i in range(trans_count):
                name = ""
                while (True):
                    char = file.read(1)
                    if (char == b"\x00"):
                        break
                    name += char.decode()
                t = Transition(name)
                self.add_transition(t)
                input_count = int.from_bytes(file.read(2), "little")
                for j in range(input_count):
                    index = int.from_bytes(file.read(2), "little")
                    arc_count = int.from_bytes(file.read(2), "little")
                    self.connect(self._places[index], t, arc_count)
                output_count = int.from_bytes(file.read(2), "little")
                for j in range(output_count):
                    index = int.from_bytes(file.read(2), "little")
                    arc_count = int.from_bytes(file.read(2), "little")
                    self.connect(self._places[index], t, arc_count, True)