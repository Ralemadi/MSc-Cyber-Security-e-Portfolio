from __future__ import annotations
from abc import ABC, abstractmethod


class NotificationObserver(ABC):

    #Publish the customer safe notification through the configured Observer implementation.
    @abstractmethod
    def update(self, message: str) -> None: ...


class ConsoleNotificationObserver(NotificationObserver):
    #Publish the customer-safe notification through the configured Observer implementation.
    def update(self, message: str) -> None:
        print(f"[NOTIFICATION] {message}")


#Observer used to collect customer-safe notifications for verification.
class CollectingNotificationObserver(NotificationObserver):
    #Test double: stores notifications instead of sending them externally.


    def __init__(self) -> None:
        self.messages: list[str] = []

    #Publish the customer safe notification through the configured Observer implementation.
    def update(self, message: str) -> None:
        self.messages.append(message)
