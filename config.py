import json

class Config:
    def __init__(self):
        self.serializer = 'pickle'
        self.getterType = None
    
    def setGetterType(self, getterType):
        self.getterType = getterType
