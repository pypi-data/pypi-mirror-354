from dataclasses import dataclass
from uuid import UUID

from ed_domain.core.aggregate_roots.base_aggregate_root import \
    BaseAggregateRoot


@dataclass
class Admin(BaseAggregateRoot):
    user_id: UUID
    first_name: str
    last_name: str
    phone_number: str
    email: str
