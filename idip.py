# IDip main module (Diplomacy state description)
# Python 3 code
# by kaw, use freely

class _NamedSet (dict):
    def __init__(self):
        dict.__init__(self)
    def add(self, duck):
        dict.__setitem__( self, duck.name, duck )
        return duck
    def __getitem__(self, name):
        return dict.__getitem__( self, name )
    def __getattr__(self, name):
        return self[ name ]
    def __iter__(self):
        return dict.values( self ).__iter__()
    def empty(self):
        return 0 == dict.__len__( self )

class GraphNode:
    def __init__(self, province):
        self.province = province
        self.links = set()
        self.initialUnit = None
    def node(self):
        return self
    def link(self, node, oneWay = False):
        self.links.add( node.node() )
        if not oneWay:
            node.node().links.add( self )
    def linkMultiple(self, links_):
        for link_ in links_:
            self.link( link_ )
    def setInitialUnit(self, nation, unit ):
        self.province.setInitialOwner( nation )
        self.initialUnit = unit

class Province:
    def __init__(self, name, displayName ):
        self.name = name
        self.displayName = displayName
        self.supplyCenter = False
        self.coasts = {}
        self.main = GraphNode( self )
        self.initialOwner = None
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
    def addCoast(self, name = "coast"):
        self.coasts[ name ] = GraphNode( self )
        return self
    def setInitialOwner( self, nation ):
        self.initialOwner = nation
    def coast(self, name = "coast"):
        return self.coasts[ name ]
    def setInitialUnit( self, nation, unit ):
        self.main.setInitialUnit( nation, unit )

class Nation:
    def __init__(self, name, displayName = None):
        self.name = name
        if not displayName:
            self.displayName = self.name
        else:
            self.displayName = displayName
        self.homeProvinces = set()
        self.initialUnits = {}
    def addHome(self, province):
        self.homeProvinces.add( province )

class Board:
    def __init__(self):
        self.provinces = _NamedSet()
        self.nations = _NamedSet()
