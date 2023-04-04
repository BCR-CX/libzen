class ZendeskException(Exception):
    def __init__(self, msg: str, status_code: int, details: dict):
        super().__init__(msg)
        self.status_code = status_code
        self.details = details

    def __str__(self):
        return f"{super().__str__()} | {self.status_code} | {str(self.details)}"
