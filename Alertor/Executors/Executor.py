
class Executor(object):
    def __init__(self):
        """Correspond to a task (like an Ebay request).
        The result is put in result variable.
        """
        self.result = None

    def execute(self):
        raise NotImplementedError()
