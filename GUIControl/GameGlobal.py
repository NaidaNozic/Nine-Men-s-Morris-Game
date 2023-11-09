class GameGlobal:
    __instance = None      

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(GameGlobal, cls).__new__(cls)
        return cls.__instance
    
    def __init__(self):
        self.global_player = 1
        self.placed = False
        self.mill_tested = False
        self.placed_index = None
        self.start = None
        self.target = None
        self.text_command = "PLAYER 1: Choose position where to place your piece: "
        self.error_message =str()