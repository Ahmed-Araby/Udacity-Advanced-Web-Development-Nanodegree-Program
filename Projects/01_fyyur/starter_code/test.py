######################## chain of responsibility pattern #########################

"""
the chain of responsibility pattern is very much like
decorator pattern instead each class / object call it's functionality first before
calling it's successor as we will decide first depends on our local result

here I combined
template design pattern
decorator like pattern
to implement chain of responsibility pattern
"""

class BaseHandelr():
    def __init__(self, id):
        self.id = id;
        self.next = None;

    def setNext(self, handlerObj):
        self.next = handlerObj;
        return;

    def handleRequest(self, requestNumber):  # template method
        if self.checkForHandling(requestNumber):
            return;
        else:
            self.passRequest(requestNumber);

    def checkForHandling(self):
        """
        custom method thet differ from a handler to another
        """
        pass

    def passRequest(self, requestNumber):
        self.next.handleRequest(requestNumber);

class defaultHandler(BaseHandelr):
    def __init__(self, id):
        super().__init__(id);

    def checkForHandling(self, requestNumber):
        print("default handler will handler this request");
        return True;

class handlerA(BaseHandelr):
    def __init__(self, id):
        super().__init__(id);

    def checkForHandling(self, requestNumber):
        if(requestNumber < 30):
            print("handled by A")
            return  True;
        return False;

class handlerB(BaseHandelr):
    def __init__(self, id):
        super().__init__(id);

    def checkForHandling(self, requestNumber):
        if(requestNumber < 20):
            print("handled by B")
            return  True;
        return False;

class handlerC(BaseHandelr):
    def __init__(self, id):
        super().__init__(id);

    def checkForHandling(self, requestNumber):
        if(requestNumber < 10):
            print("handled by C")
            return  True;
        return False;


def client():
    default = defaultHandler(0);  # leaf
    A = handlerA(1);
    A.setNext(default);

    B = handlerB(2);
    B.setNext(A);

    # C is the root of our linear tree !!
    C = handlerC(3);
    C.setNext(B);
    C.handleRequest(0);


client();