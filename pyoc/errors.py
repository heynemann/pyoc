class MessageBasedError(Exception):
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message

class ConfigureError(MessageBasedError):
    def __init__(self, message):
        super(ConfigureError, self).__init__(message)
        
    def __str__(self):
        return self.message
    
class CyclicalDependencyError(MessageBasedError):
    def __init__(self, message):
        super(CyclicalDependencyError, self).__init__(message)
        
    def __str__(self):
        return self.message
