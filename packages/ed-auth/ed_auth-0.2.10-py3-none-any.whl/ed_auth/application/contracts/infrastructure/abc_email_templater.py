from abc import abstractmethod


class ABCEmailTemplater:
    @abstractmethod
    def login(self, first_name: str, otp: str) -> str: ...
