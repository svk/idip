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
        self.words[ phrase.strip().upper() ] = token
    def scan(self, string):
        rv = None
        if not string:
            return []
        for i in range( 1, len( string ) + 1):
            prefix = string[:i]
            suffix = string[i+1:]
            try:
                token = self.words[ prefix.upper() ]
                print( "matched '{pr}'".format( pr= prefix), token )
            except KeyError:
                continue
            suffixTokens = self.scan( suffix )
            if suffixTokens == None:
                continue
            if rv:
                return None
            if not token.discard:
                rv = [token] + suffixTokens
            else:
                rv = suffixTokens
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
        for nation in self.board.nations:
            token = Token( 'nation', nation )
            self.add( nation.name, token )
        self.add( "-", Token( 'separator' ) )
        self.add( " ", Token( 'blank', discard = True ) )
        self.add( "A", Token( 'unit', 'army' ) )
        self.add( "F", Token( 'unit', 'fleet' ) )
        self.add( "C", Token( 'order', 'convoy' ) )
        self.add( "convoys", Token( 'order', 'convoy' ) )
        self.add( "convoy", Token( 'order', 'convoy' ) )
        self.add( "S", Token( 'order', 'support' ) )
        self.add( "supports", Token( 'order', 'support' ) )
        self.add( "support", Token( 'order', 'support' ) )
        self.add( "convoyed", Token( 'order', 'convoyed' ) )
        self.add( "(convoyed)", Token( 'order', 'convoyed' ) )
        self.add( "by convoy", Token( 'order', 'convoyed' ) )
        self.add( "(by convoy)", Token( 'order', 'convoyed' ) )

if __name__ == '__main__':
    from idipmap import createStandardBoard

    board = createStandardBoard()
    parser = DiplomacyParser( board )
    while True:
        lastInput = input().strip()
        print( repr( lastInput ) )
        result = parser.scan( lastInput )
        if result:
            for token in result:
                print( str(token) )
        else:
            print( "no parse" )
