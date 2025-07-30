class NonImplementedForward(Exception):
    def __init__(self):
        super().__init__(
            message="Model does not work with forward because of internal patchification and feature merging required. Please use model.run_forward() to perform predictions."
        )
