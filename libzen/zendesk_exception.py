class ZendeskException(Exception):
    def __init__(self, msg: str, status_code: int, details: dict, headers: dict[str,str] | None = None):
        Exception().__init__(msg)
        self.status_code = status_code
        self.details = details
        self.response_headers = headers or {}

    def __str__(self):
        return f"{super().__str__()} | {self.status_code} | {str(self.details)}"
