from abc import ABC, abstractmethod
class Sandwich:
    @abstractmethod
    def __init__(self) -> None:
        size: str
        cost: int
        
    