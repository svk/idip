# IDip main module (Diplomacy state description)
# Python 3 code
# by kaw, use freely

class _CaseInsensitiveString (str):
    def __hash__(self):
        return self.upper().__hash__()
    def __cmp__(self, that):
        return self.upper().__cmp__( that.upper() )
    def __eq__(self, that ):
        return self.upper().__eq__( that.upper() )

class _NamedSet (dict):
    def __init__(self):
        dict.__init__(self)
    def add(self, duck):
        dict.__setitem__( self, _CaseInsensitiveString( duck.name ), duck )
        return duck
    def __getitem__(self, name):
        return dict.__getitem__( self, _CaseInsensitiveString( name ) )
    def __getattr__(self, name):
        return self[ _CaseInsensitiveString( name ) ]
    def __iter__(self):
        return dict.values( self ).__iter__()
    def empty(self):
        return 0 == dict.__len__( self )

class GraphNode:
    def __init__(self, province, name = None, central = False):
        self.province = province
        self.links = set()
        self.unit = None
        self.name = name
        self.central = central
    def node(self):
        return self
    def link(self, node, oneWay = False):
        self.links.add( node.node() )
        if not oneWay:
            node.node().links.add( self )
    def linkMultiple(self, links_):
        for link_ in links_:
            self.link( link_ )
    def setUnit(self, nation, unit ):
        self.province.setOwner( nation )
        self.unit = unit
    def shortname(self):
        if not self.name:
            return self.province.name
        return "{province}({node})".format( province = self.province.name, node = self.name )
    def reachableBySatisfying(self, that, f):
        todo = [ self ]
        done = set(todo)
        while todo:
            next = todo.pop()
            for link in next.links:
                if link == that:
                    return True
                if f(link) and not (link in done):
                    todo.append( link )
                    done.add( link )
        return False
    def mayReachByConvoy(self, that, requireFleets = True):
        return self.reachableBySatisfying( that, lambda l : ((not requireFleets) or l.unit == 'fleet') and l.central )
    

class InvalidState:
    pass

class Province:
    def __init__(self, name, displayName ):
        self.name = name
        self.displayName = displayName
        self.supplyCenter = False
        self.coasts = {}
        self.main = GraphNode( self, central = True )
        self.owner = None
    def __repr__(self):
        return "Province({abbr}//{name})".format( abbr = self.name, name = self.displayName )
    def link(self, province):
        self.main.link( province.main )
    def node(self):
        return self.main
    def linkMultiple(self, links):
        for link_ in links:
            self.link( link_ )
    def makeSupply(self):
        self.supplyCenter = True
        return self
    def waternode(self):
        # Note: gives a WRONG result for inland provinces.
        # gives no result if a coast must be specified.
        try:
            return self.coast()
        except KeyError:
            return self.main
    def addCoast(self, name = None):
        if name:
            name = _CaseInsensitiveString( name ) 
        self.coasts[ name ] = GraphNode( self, name )
        return self
    def setOwner( self, nation ):
        self.owner = nation
    def coast(self, name = None):
        if name:
            name = _CaseInsensitiveString( name ) 
        return self.coasts[ name ]
    def setUnit( self, nation, unit ):
        self.main.setUnit( nation, unit )
    def neighbours(self):
        rv = [ n.province for n in self.main.links ]
        for coast in self.coasts.values():
            for n in coast.links:
                rv.append( n.province )
        return set(rv)
    def unitnode(self):
        if self.main.unit:
            return self.main
        for name,coast in self.coasts.items():
            if coast.unit:
                return coast
        return None
    def unitCoast(self):
        for name,coast in self.coasts.items():
            if coast.unit:
                return str(name)
        return None
    def unit(self):
        if self.main.unit:
            return self.main.unit
        for coast in self.coasts.values():
            if coast.unit:
                return coast.unit
        return None
    def clearState(self):
        self.owner = None
        self.main.unit = None
        for coast in self.coasts.values():
            coast.unit = None
    def exportState(self):
        if not self.owner:
            return ""
        rv = [ self.owner.name ]
        if self.unit():
            rv.append( { 'fleet': 'F', 'army': 'A' }[ self.unit() ] )
            if (not self.main.unit) and (len( self.coasts ) > 1):
                rv.append( self.unitCoast() )
        return rv
    def importState(self, tokens):
        try:
            owner = tokens.pop(0)
            try:
                self.owner = self.board.nations[ owner ]
            except KeyError:
                raise InvalidState()
            unit, node = None, self.main
            try:
                unit = { 'A': 'army', 'F': 'fleet' } [ tokens.pop(0) ]
                try:
                    node = self.coasts[ _CaseInsensitiveString( tokens.pop(0) ) ]
                except KeyError:
                    raise InvalidState()
            except IndexError:
                if unit == 'fleet':
                    try:
                        node = node.province.coast()
                    except KeyError:
                        pass #inelegant way of handling oceans
            node.unit = unit
        except IndexError:
            raise InvalidState()
    def mayConvoyTo(self, that, requireFleets = True):
        for fromCoast in self.coasts.values():
            for toCoast in that.coasts.values():
                if fromCoast.mayReachByConvoy( toCoast, requireFleets ):
                    return True
        return False

class Nation:
    def __init__(self, name, displayName = None):
        self.name = name
        if not displayName:
            self.displayName = self.name
        else:
            self.displayName = displayName
        self.homeProvinces = set()
    def addHome(self, province):
        self.homeProvinces.add( province )

class Board:
    def __init__(self):
        self.provinces = _NamedSet()
        self.nations = _NamedSet()
        self.provincesByDisplayName = {}
    def addNation(self, nation):
        self.nations.add( nation )
        nation.board = self
    def addProvince(self, province):
        self.provinces.add( province )
        self.provincesByDisplayName[ province.displayName.upper() ] = province
        province.board = self
    def importState(self, states):
        for province in self.provinces:
            province.clearState()
        for state in states:
            tokens = state.split()
            try:
                provinceAbbr = tokens.pop(0).strip()
                province = self.provinces[ provinceAbbr ]
            except KeyError:
                raise InvalidState()
            province.importState( tokens )
    def exportState(self):
        rv = []
        for province in self.provinces:
            tokens = province.exportState()
            if tokens:
                rv.append( " ".join( [ province.name ] + tokens ) )
        return rv
    def provinceByName(self, shortname):
        try:
            return self.provinces[ shortname ]
        except KeyError:
            pass
        try:
            return self.provincesByDisplayName[ shortname.upper() ]
        except KeyError:
            pass
        return None
    def nodeByShortname(self, shortname, selectCoastal):
        nodename = None
        if "(" in shortname:
            shortname, node = shortname.split( "(", 1 )
            if not node.endswith( ")" ):
                return None
            nodename = node[:-1]
        province = self.provinceByName( shortname )
        if not province:
            return None
        if (not selectCoastal) or (not province.coasts):
            return province.main
        try:
            return province.coast( nodename )
        except KeyError:
            return None
