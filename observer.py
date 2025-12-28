from typing import Callable
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Event[* TA, TO]:
    _subscribers: list[Callable[[*TA], TO]] = field(default_factory=list)

    @property
    def subscriber(self) -> "OnEventSubscriber[*TA, TO]":
        return OnEventSubscriber(self)

    def subscribe(self, subscriber: Callable[[*TA], TO]) -> None:
        self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber: Callable[[*TA], TO]) -> None:
        self._subscribers.remove(subscriber)

    def invoke(self, *args: *TA) -> None:
        for subscriber in self._subscribers:
            subscriber(*args)


@dataclass(frozen=True)
class OnEventSubscriber[* TA, TO]:
    _event: Event[*TA, TO]

    def subscribe(self, subscriber: Callable[[*TA], TO]) -> None:
        self._event.subscribe(subscriber)

    def unsubscribe(self, subscriber: Callable[[*TA], TO]) -> None:
        self._event.unsubscribe(subscriber)