from ONLINE_QUIZ_APPLICATION.choices import NotificationType
from ONLINE_QUIZ_APPLICATION.imports import models, settings


class DashboardActivity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dashboard_activities",
        verbose_name="User",
    )
    activity_name = models.CharField(max_length=200, verbose_name="Activity name")
    activity_date = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Activity date")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="Activity metadata")

    class Meta:
        verbose_name = "Dashboard activity"
        verbose_name_plural = "Dashboard activities"
        ordering = ["-activity_date"]
        indexes = [models.Index(fields=["user", "-activity_date"], name="activity_user_date_idx")]

    def __str__(self):
        return f"{self.user} - {self.activity_name}"


class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="User",
    )
    title = models.CharField(max_length=150, verbose_name="Title")
    message = models.TextField(verbose_name="Message")
    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.INFO,
        db_index=True,
        verbose_name="Notification type",
    )
    is_read = models.BooleanField(default=False, db_index=True, verbose_name="Read")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read", "-created_at"], name="notif_user_read_created_idx")]

    def mark_as_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=["is_read"])

    def __str__(self):
        return f"{self.title} - {self.user}"
