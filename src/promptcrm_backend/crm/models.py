from django.db import models


class PCRClientStatus(models.Model):
    id_status = models.AutoField(db_column="IdStatus", primary_key=True)
    status_description = models.CharField(db_column="StatusDescription", max_length=20)

    class Meta:
        db_table = "PCRClientStatuses"
        managed = False


class PCRClient(models.Model):
    id_client = models.AutoField(db_column="IdClient", primary_key=True)
    client_code = models.CharField(db_column="ClientCode", max_length=30)
    status = models.ForeignKey(
        PCRClientStatus,
        db_column="IdStatus",
        on_delete=models.PROTECT,
        related_name="clients",
    )
    created_at = models.DateTimeField(db_column="CreatedAt")
    updated_at = models.DateTimeField(db_column="UpdatedAt")

    class Meta:
        db_table = "PCRClients"
        managed = False