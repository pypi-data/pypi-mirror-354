class SMPparamException(Exception):
    def __init__(self, param):
        message = f"{param} is not a valid argument for smp. Please check segmentation-models-pytorch architecture, encoder and pretrained_weights valid arguments."
        super().__init__(message)
