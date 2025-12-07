from dataclasses import dataclass
from typing import List
from datetime import datetime

from django.utils import timezone
from django.core.cache import cache

from crm.models import PCRClient


@dataclass
class ClientDTO:
    id_client: int
    client_code: str
    id_status: int
    status_description: str
    created_at: datetime
    updated_at: datetime


    """
    Repository usando Django ORM sobre PCRClients.
    Prepara uso de cache a nivel de lectura.
    """


class ClientOrmRepository:


    CACHE_TTL_SECONDS = 60

    def _cache_key_clients_by_status(self, id_status: int) -> str:
        return f"clients:status:{id_status}"


    def create_client(self, client_code: str, id_status: int) -> int:
        """
        Escritura con ORM.
        Invalida cache de ese status.
        """
        now = timezone.now()

        client = PCRClient.objects.create(
            client_code=client_code,
            status_id=id_status,
            created_at=now,
            updated_at=now,
        )

        cache.delete(self._cache_key_clients_by_status(id_status))

        return client.id_client

    def get_clients_by_status(self, id_status: int, use_cache: bool = True) -> List[ClientDTO]:
        """
        Lectura con ORM.
        Usa cache opcionalmente.
        """

        cache_key = self._cache_key_clients_by_status(id_status)

        if use_cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
            
        qs = (
            PCRClient.objects
            .filter(status_id=id_status)
            .select_related("status")
            .order_by("id_client")
        )

        results: List[ClientDTO] = []

        for c in qs:
            results.append(
                ClientDTO(
                    id_client=c.id_client,
                    client_code=c.client_code,
                    id_status=c.status_id,
                    status_description=c.status.status_description,
                    created_at=c.created_at,
                    updated_at=c.updated_at,
                )
            )

        if use_cache:
            cache.set(cache_key, results, timeout=self.CACHE_TTL_SECONDS)
            
        return results



""" 
cd promptcrm_backend

.\.venv\Scripts\activate

python manage.py shell



from crm.repositories.client_orm_repository import ClientOrmRepository

repo = ClientOrmRepository()

new_id = repo.create_client(
    client_code="CLI-TEST-001",
    id_status=1,   # o 2, 3, según lo que viste en el SELECT
)

print("Nuevo cliente ORM:", new_id)


clients = repo.get_clients_by_status(1)

for c in clients:
    print(
        "IdClient:", c.id_client,
        "| Code:", c.client_code,
        "| Status:", c.status_description,
        "| CreatedAt:", c.created_at,
    )
 """
