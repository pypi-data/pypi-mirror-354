class FetchError(Exception):
    """从API拉取数据时发生的错误"""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
