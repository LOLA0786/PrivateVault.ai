class SystemGuard:
    """
    Prevents dangerous or unstable system states.
    """

    def __init__(self):
        self.safe_mode = False

    def enable_safe_mode(self):
        self.safe_mode = True

    def check(self):
        if self.safe_mode:
            raise Exception("System in SAFE MODE")
