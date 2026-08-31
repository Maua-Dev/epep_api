import uuid
from abc import ABC, abstractmethod
from typing import List

from src.shared.domain.entities.member import Member


class IMemberRepository(ABC):

    @abstractmethod
    def get_member(self, member_id: uuid.UUID) -> Member:
        """
        If member not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def get_all_member(self) -> List[Member]:
        pass

    @abstractmethod
    def create_member(self, new_member: Member) -> Member:
        pass

    @abstractmethod
    def delete_member(self, member_id: uuid.UUID) -> Member:
        """
        If member not found raise NoItemsFound
        """
        pass

    @abstractmethod
    def update_member(self, member: Member) -> Member:
        """
        If member not found raise NoItemsFound
        """
        pass
