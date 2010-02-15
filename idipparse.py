
# Long or short names can be used interchangeably.
# All army/fleet prefixes are optional.
# Patterns for hold orders:
#    A Mun-Holds
#    A Mun H
#    A Mun
# Patterns for movement orders:
#    A Mun-Sil
# Patterns for 


class Token:
    def __init__(self, kind, argument = None, discard = False):
        self.kind = kind
        self.argument = argument
        self.discard = discard
    def __str__(self):
        return "{kind}//{arg}".format( kind = self.kind, arg = self.argument )

class Parser:
    def __init__(self):
        self.words = {}
    def add(self, phrase, token):
        self.words[ phrase.upper() ] = token
    def scan(self, string):
        if not string:
            yield []
        for i in range( len( string ), 0, -1):
            prefix = string[:i]
            suffix = string[i:]
            try:
                token = self.words[ prefix.upper() ]
            except KeyError:
                continue
            suffixAlternatives = self.scan( suffix )
            if not suffixAlternatives:
                continue
            for suffixAlternative in suffixAlternatives:
                if not token.discard:
                    yield [token] + suffixAlternative
                else:
                    yield suffixAlternative
        raise StopIteration
    def firstParse(self, string):
        rv = None
        for rv in self.scan( string ):
            break
        return rv
    def uniqueParse(self, string):
        rv = None
        for x in self.scan( string ):
            if rv:
                return None
            rv = x
        return rv

class DiplomacyParser (Parser):
    def __init__(self, board):
        Parser.__init__(self)
        self.board = board
        for province in self.board.provinces:
            token = Token( 'province', province )
            self.add( province.name, token )
            self.add( province.displayName, token )
            for alternate in province.alternateNames:
                self.add( alternate, token )
            for coastName in province.coasts.keys():
                coastName = str( coastName )
                if coastName != None:
                    # note multiple coasts with same name map to same token
                    # a coast token is a specifier, not a node
                    token = Token( 'named-coast', coastName )
                    self.addBracketed( coastName, token )
        for nation in self.board.nations:
            token = Token( 'nation', nation )
            self.add( nation.name, token )
            self.add( nation.adjective, token )
        self.add( "-", Token( 'separator' ) )
        self.add( "--", Token( 'separator' ) )
        self.add( "to", Token( 'separator' ) )
        self.add( "->", Token( 'separator' ) )
        self.add( " ", Token( 'blank', discard = True ) )
        self.add( "A", Token( 'unit', 'army' ) )
        self.add( "F", Token( 'unit', 'fleet' ) )
        self.add( "army", Token( 'unit', 'army' ) )
        self.add( "fleet", Token( 'unit', 'fleet' ) )
        self.add( "C", Token( 'order', 'convoy' ) )
        self.add( "convoys", Token( 'order', 'convoy' ) )
        self.add( "convoy", Token( 'order', 'convoy' ) )
        self.add( "S", Token( 'order', 'support' ) )
        self.add( "H", Token( 'order', 'hold' ) )
        self.add( "holds", Token( 'order', 'hold' ) )
        self.add( "hold", Token( 'order', 'hold' ) )
        self.add( "supports", Token( 'order', 'support' ) )
        self.add( "support", Token( 'order', 'support' ) )
        self.add( "build", Token( 'order', 'build' ) )
        self.add( "disband", Token( 'order', 'disband' ) )
        self.add( "disbands", Token( 'order', 'disband' ) )
        self.add( "destroy", Token( 'order', 'disband' ) )
        self.add( "destroyed", Token( 'order', 'disband' ) )
        self.add( "cha", Token( 'xxx', 'zzz' ) )
        self.addBracketed( "convoyed", Token( 'order', 'convoyed' ) )
        self.addBracketed( "by convoy", Token( 'order', 'convoyed' ) )
        self.addStandardCoastSynonyms()
    def addStandardCoastSynonyms(self):
        for direction in [ "north", "east", "west", "south" ]:
            letter = direction[0]
            token = Token( 'named-coast', letter + "c" )
            self.addBracketed( "{direction} coast".format( direction = direction ), token )
            self.addBracketed( "{direction}coast".format( direction = direction ), token )
            self.addBracketed( "{direction}".format( direction = direction ), token )
            self.addBracketed( "{letter}. coast".format( letter = letter ), token )
            self.addBracketed( "{letter} coast".format( letter = letter ), token )
            self.addBracketed( "{letter}.c.".format( letter = letter ), token )
            self.addBracketed( "{letter}. c.".format( letter = letter ), token )
            self.addBracketed( "{letter} c".format( letter = letter ), token )
            self.addBracketed( "{letter}c".format( letter = letter ), token )
    def addBracketed(self, phrase, token, noPlain = False):
        if not noPlain:
            self.add( phrase, token )
        self.add( "({s})".format( s = phrase ), token )
        self.add( "[{s}]".format( s = phrase ), token )
        self.add( "[{s}]".format( s = phrase ), token )
        

if __name__ == '__main__':
    from idipmap import createStandardBoard

    board = createStandardBoard()
    parser = DiplomacyParser( board )
    while True:
        lastInput = input().strip()
        print( repr( lastInput ) )
        results = parser.scan( lastInput )
        for result in results:
            print( "PARSE" )
            for token in result:
                print( "\t", str(token) )
            print()
        print( "FIRST-PARSE" )
        result = parser.firstParse( lastInput )
        if not result:
            print( result )
        else:
            for token in result:
                print( "\t", str(token) )
        print()
        print( "UNIQUE-PARSE" )
        result = parser.uniqueParse( lastInput )
        if not result:
            print( result )
        else:
            for token in result:
                print( "\t", str(token) )
        print()
