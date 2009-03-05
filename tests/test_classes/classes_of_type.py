class Base(object):
    def __init__(self):
        pass
    
class InheritorA(Base):
    def __init__(self):
        self.title = "a"
    
class InheritorB(Base):
    def __init__(self):
        pass
    
class AllItems(object):
    def __init__(self, all_classes):
        self.all_classes = all_classes
