class BlindPayError(Exception):
    """BlindPay SDK error"""

    def __init__(self, message: str):
        super().__init__(message)
        self.name = "BlindpayError"
