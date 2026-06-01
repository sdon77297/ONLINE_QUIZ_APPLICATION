from ONLINE_QUIZ_APPLICATION.imports import models, settings


class LoginHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="login_history",
        verbose_name="User",
    )
    login_time = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Login time")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP address")
    user_agent = models.TextField(blank=True, verbose_name="User agent")
    was_successful = models.BooleanField(default=True, verbose_name="Successful login")

    class Meta:
        verbose_name = "Login history"
        verbose_name_plural = "Login history"
        ordering = ["-login_time"]
        indexes = [models.Index(fields=["user", "-login_time"], name="login_user_time_idx")]

    def __str__(self):
        return f"{self.user} - {self.login_time}"
