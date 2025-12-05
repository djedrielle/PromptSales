from dataclasses import dataclass
from typing import List, Optional
from django.db import connection


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
    def create_subscription(
        self,
        id_user: int,
        id_tier: int,
        start_date,
        end_date,
        enabled: bool = True,
    ) -> int:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DECLARE @NewIdSub INT;

                EXEC SP_PCR_CreateSubscription
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
            return int(row[0])


    def get_active_by_user(self, id_user: int) -> List[SubscriptionDTO]:
        """
        Llama a dbo.PCR_GetActiveSubscriptionsByUser y devuelve una lista de DTO.
        """
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
        return results