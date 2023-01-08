class ChessError(Exception):
    pass

class Check(ChessError):
    pass

class CheckMate(ChessError):
    pass

class Draw(ChessError):
    pass

class InvalidMove(ChessError):
    pass

class NotYourTurn(ChessError):
    pass 
