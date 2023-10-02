class Story:

    def __init__(self):
        self.chapters = []
        self.title = None
        self.sypnop = None
        self.character_context = None
        self.outline = None

    def add_chapter(self, chapter, identifier):
        self.chapters.append([chapter, identifier])
    
    def set_title(self, title):
        self.title = title
    
    def set_sypnop(self, sypnop):
        self.sypnop = sypnop
    
    def set_character_context(self, character_context):
        self.character_context = character_context

    def set_outline(self, outline):
        self.outline = outline

    def get_plaintext(self):
        fulltxt = ''
        if self.title:
            fulltxt += f"{self.title}\n\n\n"
        for chapter, name in self.chapters:
            fulltxt += f"{name}\n{chapter}\n\n"
        return fulltxt
