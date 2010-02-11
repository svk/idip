class MovementOrder:
    def __init__(self, source,
                       destination = None,
                       supportSource = None, supportDestination = None,
                       convoySource = None, convoyDestination = None):
        self.destination = self.source = source
        if destination:
            self.destination = destination
        self.supportSource = supportSource
        self.supportDestination = supportDestination
        self.support = self.supportSource != None
        self.convoySource = convoySource
        self.convoyDestination = convoyDestination
        self.convoy = self.convoySource != None
        assert (self.supportDestination == None) == (self.supportSource == None)
        assert (self.convoyDestination == None) == (self.convoySource == None)
        assert not (self.support and self.convoy)
    def __str__(self):
        if self.support:
            rv = "{unitType} {source} S {suppSource}--{suppDest}"
        elif self.convoy:
            rv = "{unitType} {source} C {convSource}--{convDest}"
        elif self.source == self.destination:
            rv = "{unitType} {source}--Holds"
        else:
            rv = "{unitType} {source}--{dest}"
        unitType = { 'fleet': 'F', 'army': 'A', None: '?' }[ self.source.unit ]
        try:
            suppSource = self.supportSource.shortname()
            suppDest = self.supportDestination.shortname()
        except AttributeError:
            suppSource, suppDest = None, None
        try:
            convSource = self.convoySource.shortname()
            convDest = self.convoyDestination.shortname()
        except AttributeError:
            convSource, convDest = None, None
        return rv.format(
            unitType = unitType,
            suppSource = suppSource,
            suppDest = suppDest,
            convSource = convSource,
            convDest = convDest,
            source = self.source.shortname(),
            dest = self.destination.shortname()
        )
    def illegality(self):
        things = int( self.convoy ) + int( self.support ) + int( self.source != self.destination )
        if things > 1:
            return "invalid move"
        if not self.source.unit:
            return "no such unit"
        unitType = self.source.unit
        if self.support:
            # Must be able to move into the square against which the attack
            # is being supported.
            if not self.supportDestination in self.source.links:
                
                return "{unitType} cannot support {to} from {fr}".format(
                    unitType = unitType,
                    to = self.supportDestination.shortname(),
                    fr = self.source.shortname(),
                )
            return ""
        if self.convoy:
            if unitType != 'fleet':
                return "cannot convoy with non-fleet"
            if self.source.province.unitCoast() != None:
                return "cannot convoy along coast"
            if not self.convoyDestination in self.source.links:
                return "not adjacent to convoy destination"
            if not self.convoySource in self.source.links:
                return "not adjacent to convoy source"
            return ""
        if not self.destination in self.source.links:
            if self.destination.province in self.source.province.neighbours():
                return {
                    'fleet': 'not adjacent along coast to destination',
                    'army': 'army cannot move into the sea',
                }[ unitType ]
            return "not adjacent to destination"
        return ""

def interpretPair( board, s, selectCoastal, noHold = False):
    if "--" in s:
        first, last = s.split( "--", 1 )
    else:
        try:
            first, last = s.split( "-", 1 )
        except TypeError:
            return None
        except ValueError:
            return None
    if not noHold:
        if last.upper() == "HOLDS" or last.upper() == "HOLD":
            last = first
    first = board.nodeByShortname( first, selectCoastal )
    last = board.nodeByShortname( last, selectCoastal )
    if (first == None) or (last == None):
        return None
    return first, last

def interpretMovementOrder( board, s ):
    tokens = s.split()
    if not tokens: return None
    dest = None
    try:
        unitType = { 'A': 'army', 'F': 'fleet' } [ tokens[0] ]
        selectCoastal = unitType == 'fleet'
        tokens.pop(0)
    except KeyError:
        unitType = None
        selectCoastal = False
    if not tokens: return None
    try:
        source, dest = interpretPair( board, tokens[0], selectCoastal )
        if unitType == None:
            unitType = source.province.unit()
            if unitType == None:
                return None
            selectCoastal = unitType == 'fleet'
            source, dest = interpretPair( board, tokens[0], selectCoastal )
        return MovementOrder( source, destination = dest )
    except TypeError:
        pass
    source = board.nodeByShortname( tokens[0], selectCoastal )
    tokens.pop(0)
    if not tokens: return None
    moveType = tokens[0]
    tokens.pop(0)
    if not tokens: return None
    if moveType.upper() in [ "C", "CONVOY", "CONVOYS" ]:
        ms, md = interpretPair( board, tokens[0], selectCoastal, noHold = True )
        return MovementOrder( source, convoySource = ms, convoyDestination = md )
    if moveType.upper() in [ "S", "SUPPORT", "SUPPORTS" ]:
        ms, md = interpretPair( board, tokens[0], selectCoastal )
        return MovementOrder( source, supportSource = ms, supportDestination = md )
    return None

if __name__ == '__main__':
    from idipmap import createStandardBoard
    board = createStandardBoard()
    for line in board.exportState():
        print( line )
    print()
    while True:
        data = input()
        order = interpretMovementOrder( board, data )
        if order:
            print( str(order) )
            illegality = order.illegality()
            if illegality:
                print( illegality )
        else:
            print( "No interpretation." )
