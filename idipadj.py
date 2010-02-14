class MovementOrder:
    def __init__(self, source,
                       destination = None,
                       supportSource = None, supportDestination = None,
                       convoySource = None, convoyDestination = None,
                       byConvoy = False):
        self.destination = self.source = source
        if destination:
            self.destination = destination
        self.supportSource = supportSource
        self.supportDestination = supportDestination
        self.support = self.supportSource != None
        self.convoySource = convoySource
        self.convoyDestination = convoyDestination
        self.convoy = self.convoySource != None
        self.byConvoy = byConvoy
        assert (self.supportDestination == None) == (self.supportSource == None)
        assert (self.convoyDestination == None) == (self.convoySource == None)
        assert not (self.support and self.convoy)
        assert not (self.byConvoy and (self.destination == self.source))
    def makeHold(self):
        self.destination = self.source
        self.convoySource, self.convoyDestination = None, None
        self.supportSource, self.supportDestination = None, None
        self.byConvoy, self.convoy, self.support = False, False, False
    def __str__(self):
        if self.support:
            rv = "{unitType} {source} S {suppSource}--{suppDest}"
        elif self.convoy:
            rv = "{unitType} {source} C {convSource}--{convDest}"
        elif self.source == self.destination:
            rv = "{unitType} {source}--Holds"
        elif self.byConvoy:
            rv = "{unitType} {source}--{dest} (convoyed)"
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
            # Must be able to move into the PROVINCE against which the attack
            # is being supported.
            if self.supportDestination == self.source:
                return "cannot support to own sector"
            if not self.supportDestination.province in [ link.province for link in self.source.links]:
                return "cannot support to inaccessible sector"
            return ""
        if self.convoy:
            if unitType != 'fleet':
                return "cannot convoy with non-fleet"
            convoyedUnitType = self.convoySource.unit
            if convoyedUnitType == None:
                return "no unit there to convoy"
            if convoyedUnitType != 'army':
                return "only armies can be convoyed"
            if self.source.province.unitCoast() != None:
                return "cannot convoy along coast"
            if not self.convoySource.province.mayConvoyTo( self.convoyDestination.province ):
                if self.convoySource.province.mayConvoyTo( self.convoyDestination.province, requireFleets = False):
                    return "convoy cannot succeed"
                return "convoy cannot succeed - provinces do not border the same ocean"
            return ""
        if not self.byConvoy:
            if self.destination == self.source:
                return ""
            if not self.destination in self.source.links:
                if self.destination.province in self.source.province.neighbours():
                    return {
                        'fleet': 'not adjacent along coast to destination',
                        'army': 'army cannot move into the sea',
                    }[ unitType ]
                return "not adjacent to destination"
        else:
            if not self.source.province.mayConvoyTo( self.destination.province ):
                if self.source.province.mayConvoyTo( self.destination.province, requireFleets = False):
                    return "fleets not in place for convoy"
                return "convoy between provinces not adjacent to the same ocean"
        return ""
    def nationality(self):
        return self.source.owner

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
            # Note: this is a bit too tolerant for DATC 6a4
            last = first
    first_ = board.nodeByShortname( first, selectCoastal )
    last_ = board.nodeByShortname( last, selectCoastal )
    if (first_ == None) or (last_ == None):
        if first_ == None:
            print( "Unable to resolve", first )
        if last_ == None:
            print( "Unable to resolve", last )
        return None
    return first_, last_

def interpretMovementOrder( board, s ):
    # TODO:
    #   - accept (convoy) at the end
    #   - accept A/F specifier of supported unit
    #   - accept long names for provinces, possibly including spaces
    #   - accept (and discard?) explicit convoy path specifiers:
    #         A Bre-Eng-Nth-Nwy
    #     instead of
    #         A Bre-Nwy (convoy)
    #   - XXX convoys are specified by army movement, not piecewise
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
        tokens.pop(0)
        byConvoy = False
        if tokens:
            if tokens[0].upper() in [ "(C)", "(CONVOY)", "(CONVOYED)" ]:
                byConvoy = True
        if len( tokens ) > 1: return None
        return MovementOrder( source, destination = dest, byConvoy = byConvoy )
    except TypeError:
        pass
    source = board.nodeByShortname( tokens[0], selectCoastal )
    if unitType == None:
        unitType = source.province.unit()
        if unitType == None:
            return None
        selectCoastal = unitType == 'fleet'
        source = board.nodeByShortname( tokens[0], selectCoastal )
    tokens.pop(0)
    if not tokens: return None
    moveType = tokens[0]
    tokens.pop(0)
    if not tokens: return None
    if len( tokens ) > 1: return None
    if moveType.upper() in [ "C", "CONVOY", "CONVOYS" ]:
        ms, md = interpretPair( board, tokens[0], selectCoastal = False, noHold = True )
        return MovementOrder( source, convoySource = ms, convoyDestination = md )
    if moveType.upper() in [ "S", "SUPPORT", "SUPPORTS" ]:
        ms, md = interpretPair( board, tokens[0], selectCoastal )
        selectCoastal = ms.province.unit() == 'fleet'
        ms, md = interpretPair( board, tokens[0], selectCoastal )
        return MovementOrder( source, supportSource = ms, supportDestination = md )
    return None

class UndeterminedException (BaseException):
    pass

class Dependency:
    def __init__(self, provinces, f):
        # a non-convoyed move is independent
        # a convoyed move is dependent on all the fleets ordered to convoy
        #  that could possibly convoy it, determined when either enough are
        #  dislodged to exclude  a convoy or enough are secure to guarantee
        #  one
        # a support move is dependent on its originating province
        self.provinces = provinces
        self.f = f
    def __call__(self):
        return self.f()

always = Dependency( provinces = [], f = lambda : True )
never = Dependency( provinces = [], f = lambda : False )
    
class Force:
    def __init__(self, name, condition = always, doAdd = True):
        self.name = name
        self.finalizedSupporters = 0
        self.dependentSupporters = []
        if doAdd:
            self.add( condition )
    def add(self, condition = always):
        self.dependentSupporters.append( condition )
    def tryFinalize(self):
        for condition in self.dependentSupporters:
            try:
                if condition():
                    self.finalizedSupporters += 1
                self.dependentSupporters.remove( condition )
            except UndeterminedException:
                pass
    def minimum(self):
        self.tryFinalize()
        return self.finalizedSupporters
    def maximum(self):
        self.tryFinalize()
        return self.finalizedSupporters + len( self.dependentSupporters )
    def strength(self):
        self.tryFinalize()
        if self.dependentSupporters:
            raise UndeterminedException()
        return self.finalizedSupporters
    def dependencies(self):
        rv = set()
        self.tryFinalize()
        for supporter in self.dependentSupporters:
            for dependency in supporter.provinces:
                rv.add( dependency )
        return rv

# a move order (no convoy): certain (check: move cycles)
# a support order: support dependent on no attack to supporter from flank
#                  and no successful attack to supporter from border
# move order (convoy): dependent

class MovementTurn:
    def __init__(self, board):
        self.board = board
        self.battles = {}
        for province in self.board.provinces:
            self.battles[ province.name ] = Battle( self, province )
        self.movement = [] # list of pairs of provinces
        self.retreats = [] # list of provinces
    def tryResolveSimple(self):
        somethingWorked = True
        while somethingWorked:
            somethingWorked = False
            for battle in self.unresolved():
                if battle.tryResolveSimple():
                    somethingWorked = True
    def unresolved(self):
        return filter( lambda x: not x.resolved, self.battles.values() )
    def preprocessOrders(self, orders):
        # assumed: these orders have been checked for legality and access control (nationality)
        byprov = {}
        for x in [province.name for province in self.board.provinces if province.unitnode() != None ]:
            byprov[x] = None
        for order in orders:
            byprov[ order.source.province.name ] = order
        for name, order in byprov.items():
            if order == None:
                p = self.board.provinces[name].unitnode()
                byprov[ name ] = MovementOrder( source = p, destination = p )
        return byprov
    def addOrders(self, byprov):
        # First pass: convoy orders, to source
        for order in byprov.values():
            if order.convoy:
                self.battles[ order.source.province.name ].addConvoy( order )
        # Second pass: movement orders, to destination
        for order in byprov.values():
            if order.source != order.destination:
                self.battles[ order.destination.province.name ].addMove( order )
            else:
                # anything that doesn't move implicitly holds - even things that are supporting,
                # convoying, etc.
                self.battles[ order.destination.province.name ].addHold()
        # Third pass: support orders, to support destination
        for order in byprov.values():
            if order.support:
                self.battles[ order.supportDestination.province.name ].addSupport( order )

class Battle:
    def __init__(self, turn, province):
        self.turn = turn
        self.name = province.name
        self.province = province
        self.attackers = {}
        self.defenders = Force( self.name, doAdd = False )
        self.convoyFrom = None
        self.convoyTo = None
        self.resolved = False
        self.defending = False # also means "supportable"
    def dependencies(self):
        rv = set()
        for force in self.attackers.values():
            for dep in force.dependencies():
                rv.add( dep )
        for dep in self.defenders.dependencies():
            rv.add( dep )
        return rv
    def addConvoy(self, order):
        self.convoyFrom = order.convoySource.province.name
        self.convoyTo = order.convoyDestination.province.name
    def addMove(self, order):
        # if moving, attacker on destination
        # convoyed moves must be added _after_ convoys
        # moving should also add a conditional hold in source, dependent on
        #  the attack not succeeding.
        # done. HOWEVER - this is not supportable, because the unit did not actually hold.
        # we do NOT set the defending flag!
        assert self.province == order.destination.province
        name = order.source.province.name
        if order.source == order.destination:
            raise "foo"
        defDep = Dependency( provinces = [ self ], f = lambda : not self.beingDislodged() )
        self.turn.battles[ order.source.province.name ].defenders.add( defDep )
        condition = always
        if order.byConvoy:
            condition = self.turn.battles[ name ].makeConvoyedDependency( self.province )
        self.attackers[ name ] = Force( name, condition )
    def addHold(self):
        # if holding, defender on source, unconditional
        self.defenders.add()
        self.defending = True
    def addSupport(self, order):
        # if supporting, support on support destination
        # support orders must be added _after_ move/hold orders
        if order.supportSource == order.supportDestination:
            side = self.defenders
        else:
            sourceName = order.supportSource.province.name
            side = self.attackers[ sourceName ]
        condition = self.turn.battles[ order.source.province.name ].makeSupportDependency( order.supportDestination.province )
        try:
            side.add( condition )
        except KeyError:
            pass # support order failed; no such attack/hold
    def tryResolveSimple(self):
        if self.resolved:
            return False
        try:
            if self.beingDislodged():
                # strongest attacker succeeds
                name, attacker = max( self.attackers.items(), key = lambda ab : ab[1].strength() )
                self.turn.movement.append( (name, self.name) )
                if self.defenders.strength() > 0:
                    self.turn.retreats.append( self.name )
                print( "In", self.name, "attack succeeds", self.defenders.strength() )
            else:
                # nothing moves
                print( "In", self.name, "attack fails", self.defenders.strength() )
                pass
            if self.defenders.strength() > 0 and len( self.attackers ):
                print( "resolved", self.name, self.defenders.strength() )
                for name, force in self.attackers.items():
                    print( "attacker", name, force.strength() )
            self.resolved = True
            return True
        except UndeterminedException:
            pass
    def beingDislodged(self):
        # first, disregard inferior or equal forces to the defenders
        # if none are left, we are safe
        # while there are attackers left, look at the best attacker(s):
        #   if there are multiple, we are safe (return)
        #   else we have single best attacker
        #   if this is friendly, we are safe (return)
        #   if it has friendly support, reduce its strength by one
        #   else we are dislodged (return)
        # we are safe (return)
        # note this may raise UndeterminedException
        # XXX not yet implemented fully!
        atts = {}
        defense = self.defenders.strength()
        for attacker in self.attackers.values():
            strength = attacker.strength()
            if strength > defense:
                atts[ attacker.name ] = strength
            if defense == 0:
                return True
        while atts:
            bestVal = max( atts.values() )
            bestVals = list( filter( lambda ab : ab[1] == bestVal, atts.items() ) )
            if len(bestVals) > 1:
                # attackers bounce
                return False
            bestVal = bestVals[0]
            bestValName, bestValStrength = bestVal
            bestAtt = self.turn.board.provinces[ bestValName ].owner
            ourOwner = self.turn.board.provinces[ self.name ].owner
            if bestAtt == ourOwner:
                # never dislodged by friendly attacker
                return False
            if False: # TODO handle friendly support, dropping it one at a time
                pass 
            else:
                return True
        return False
    def makeSupportDependency(self, against):
        def f():
            for name,force in self.attackers.items():
                if self.turn.board.provinces[ name ].owner == self.province.owner:
                    continue
                if name != against.name:
                    if force.strength() > 0:
                        return False
            # Obscure case: being attacked by a superior force, but not being
            #  dislodged because of a self-standoff by two even stronger forces.
            #  Requires eight neighbours.
            #  England:
            #     F ENG S Gas-Bre
            #     F NTH-ENG
            #     F Bel S NTH-ENG
            #     F Lon S NTH-ENG
            #     F MAO-ENG
            #     F IRI S MAO-ENG
            #     F Wal S MAO-ENG
            #  France:
            #     F Bre-ENG
            #     F Pic S Bre-ENG
            #     A Par-Bre
            #  Italy:
            #     A Gas-Bre
            #  Result should be Gascony moving into Brest, not standoff with Paris.
            return not self.beingDislodged()
        return Dependency( provinces = [self], f = f )
    def makeConvoyedDependency(self, towards):
        todo = []
        def willConvoy( link ):
            if not link.central:
                return False
            if not link.unit == 'fleet':
                return False
            if self.turn.battles[ link.province.name ].convoyFrom != self.name:
                return False
            if self.turn.battles[ link.province.name ].convoyTo != towards.name:
                return False
            return True
        for coast in self.province.coasts.values():
            for link in filter( willConvoy, coast.links ):
                todo.append( link )
        done = set(todo)
        while todo:
            next = todo.pop()
            for link in filter( willConvoy, next.links ):
                if link in done: continue
                todo.append( link )
                done.add( link )
        reachable = False
        for ocean in done:
            for link in ocean.links:
                if link.province == towards:
                    reachable = True
        if not reachable:
            return Dependency( provinces = [], f = lambda : False )
        dependencies = []
        for node in done:
            if willConvoy( node ):
                dependencies.append( self.turn.battles[ node.province.name ] )
        def canReach():
            goodConvoys = []
            okayConvoys = []
            for convoy in dependencies:
                try:
                    if not self.turn.battles[ convoy.name ].beingDislodged():
                        goodConvoys.append( convoy.name )
                        okayConvoys.append( convoy.name )
                except UndeterminedException:
                    okayConvoys.append( convoy.name )
            visiting = [ self.name ]
            visited = set( visiting )
            okayReach = False
            while visiting:
                next = visiting.pop()
                if next == towards.name:
                    okayReach = True
                    break
                outlinks = filter( lambda x: (x == towards.name) or ((x in okayConvoys) and not (x in visited)),
                  [ province.name for province in self.turn.board.provinces[ next ].neighbours() ]
                  )
                outlinks = list( outlinks )
                for outlink in outlinks:
                    visiting.append( outlink )
                    visited.add( outlink )
            if not okayReach:
                return False
            # ahoy there, code duplication ahead
            visiting = [ self.name ]
            visited = set( visiting )
            goodReach = False
            while visiting:
                next = visiting.pop()
                if next == towards.name:
                    goodReach = True
                    break
                outlinks = filter( lambda x: (x == towards.name) or ((x in goodConvoys) and not (x in visited)),
                  [ province.name for province in self.turn.board.provinces[ next ].neighbours() ]
                  )
                outlinks = list( outlinks )
                for outlink in outlinks:
                    visiting.append( outlink )
                    visited.add( outlink )
            if goodReach:
                return True
            raise UndeterminedException()
        return Dependency( provinces = dependencies, f = canReach )

# How to resolve the "complicated" cases?
# For convoys: a convoyed army in a cycle cannot cut support
# Rule 21: When a convoy cycle (the only sort of dependency
#          cycle remaining after elimination of move-cycles, check)
#          is detected, remove all conditional attacks against 
#          supporters of attacks against convoys by units having
#          those convoys as potential convoyers.
# Rule 22: This should succeed automatically; there is no cycle
#          if there is at least one guaranteed successful route.


# TODO
#  - generate plaintext summary of adjudication
#  - check support is correct
#  - head on collisions, 
#  - movement cycles, "all or none"
#  - convoy paradox handling
#  - generate next state, & implement build & retreat orders


        
        
if __name__ == '__main__':
    from idipmap import createStandardBoard
    board = createStandardBoard()

    print( "State of the board:" )
    for line in board.exportState():
        print( "\t", line )
    print()

    print( "Input state, end with empty line." )
    state = []
    while True:
        lastInput = input()
        if not lastInput: break
        state.append( lastInput )
    board.importState( state )

    print( "State of the board:" )
    for line in board.exportState():
        print( "\t", line )
    print()

    print( "Input orders, end with an empty line." )
    orders = []
    try:
        while True:
            lastInput = input()
            if not lastInput:
                break
            if lastInput.startswith( "#" ):
                print( lastInput )
            else:
                order = interpretMovementOrder( board, lastInput )
                print( "Order:", order)
                if order.illegality():
                    print( "ignoring illegal move:", order.illegality() )
                    order.makeHold()
                orders.append( order )
    except EOFError:
        pass
    turn = MovementTurn( board )
    byprov = turn.preprocessOrders( orders )
    turn.addOrders( byprov )
    print()

    print( "Attempting to resolve." )

    turn.tryResolveSimple()

    unresolvedBattles = list( turn.unresolved() )
    for battle in unresolvedBattles:
        print( "Unresolved:", battle.province.displayName )
    if not unresolvedBattles:
        print()
        moves, retreats =  0, 0
        for alpha, omega in turn.movement:
            pFrom = board.provinces[ alpha ]
            pTo = board.provinces[ omega ]
            print( "MOVE", pFrom.displayName, pTo.displayName )
            moves += 1
        for alpha in turn.retreats:
            pFrom = board.provinces[ alpha ]
            print( "RETREAT", pFrom.displayName )
            retreats += 1
        print( "{moves} moves and {retreats} retreats".format( moves = moves, retreats = retreats ) )
