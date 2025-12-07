from dataclasses import dataclass
from typing import List, Optional
from django.db import connection
from django.core.cache import cache


@dataclass
class SubscriptionDTO:
    id_subscription: int
    id_user: int
    id_tier: int
    tier_name: str
    pricing: float
    start_date: Optional[str]
    end_date: Optional[str]
    enabled: bool
    created_at: str
    updated_at: str


class SubscriptionSpRepository:
    """
    Repository con SPs.
    Aquí dejamos previstas de cache y usamos django.db.connection,
    que ya usa connection pooling en DATABASES[default].CONN_MAX_AGE.
    """

    CACHE_TTL_SECONDS = 60

    def _cache_key_active_by_user(self, id_user: int) -> str:
        return f"subscriptions:active:user:{id_user}"

    def create_subscription(
        self,
        id_user: int,
        id_tier: int,
        start_date,
        end_date,
        enabled: bool = True,
    ) -> int:
        """
        Llama a dbo.SP_PCR_CreateSubscription y devuelve el IdSubscription generado.
        Invalida la cache de suscripciones activas del usuario.
        """
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DECLARE @NewIdSub INT;

                EXEC dbo.SP_PCR_CreateSubscription
                    @IdUser    = %s,
                    @IdTier    = %s,
                    @StartDate = %s,
                    @EndDate   = %s,
                    @Enabled   = %s,
                    @NewIdSub  = @NewIdSub OUTPUT;

                SELECT @NewIdSub;
                """,
                [id_user, id_tier, start_date, end_date, int(enabled)],
            )
            row = cursor.fetchone()
            new_id = int(row[0])

        # invalidar cache fuera del with
        cache.delete(self._cache_key_active_by_user(id_user))

        return new_id

    def get_active_by_user(self, id_user: int, use_cache: bool = True) -> List[SubscriptionDTO]:
        """
        Llama a dbo.SP_PCR_GetActiveSubscriptionsByUser y devuelve una lista de DTO.
        Usa cache si use_cache es True.
        """
        cache_key = self._cache_key_active_by_user(id_user)

        if use_cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached

        with connection.cursor() as cursor:
            cursor.execute(
                "EXEC dbo.SP_PCR_GetActiveSubscriptionsByUser @IdUser = %s;",
                [id_user],
            )
            cols = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

        results: List[SubscriptionDTO] = []
        for r in rows:
            data = dict(zip(cols, r))
            results.append(
                SubscriptionDTO(
                    id_subscription=data["IdSubscription"],
                    id_user=data["IdUser"],
                    id_tier=data["IdTier"],
                    tier_name=data["TierName"],
                    pricing=float(data["Pricing"]),
                    start_date=data["StartDate"],
                    end_date=data["EndDate"],
                    enabled=bool(data["Enabled"]),
                    created_at=data["CreatedAt"],
                    updated_at=data["UpdatedAt"],
                )
            )

        if use_cache:
            cache.set(cache_key, results, timeout=self.CACHE_TTL_SECONDS)

        return results

""" 
cd promptcrm_backend

.\.venv\Scripts\activate

python manage.py shell



 
from datetime import date, timedelta
from crm.repositories.subscription_sp_repository import SubscriptionSpRepository

repo = SubscriptionSpRepository()

# usa IdUser e IdTier que EXISTAN en la base
new_id = repo.create_subscription(
    id_user=4, 
    id_tier=2,
    start_date=date.today(),
    end_date=date.today() + timedelta(days=30),
)

print("Id nueva subscripción:", new_id)  









      
from crm.repositories.subscription_sp_repository import SubscriptionSpRepository

repo = SubscriptionSpRepository()

# usa un IdUser válido
user_id = 4 

subs = repo.get_active_by_user(user_id)

for s in subs:
    print("IdSub:", s.id_subscription,
          "Tier:", s.tier_name,
          "Precio:", s.pricing,
          "Inicio:", s.start_date,
          "Fin:", s.end_date,
          "Enabled:", s.enabled)
     

""" 