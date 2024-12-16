from django.db import models

class LineSettings(models.Model):
    LINE_CHOICES = [
        ('1', 'Линия 1'),
        ('2', 'Линия 2'),
        ('3', 'Линия 3'),
        ('4', 'Линия 4'),
        ('5', 'Линия 5'),
    ]

    line_name = models.CharField(max_length=10, choices=LINE_CHOICES, verbose_name="Название линии")
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    fixation_time = models.PositiveIntegerField(default=5, verbose_name="Время фиксации (мин)")

    def __str__(self):
        return f"{self.get_line_name_display()} (Активна: {self.is_active})"


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class DowntimeReason(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='reasons')
    reason = models.CharField(max_length=100)

    def __str__(self):
        return self.reason


# Новая модель для участков
class Section(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название участка")
    line = models.ForeignKey(LineSettings, on_delete=models.CASCADE, related_name="sections", verbose_name="Линия")
    is_active = models.BooleanField(default=True, verbose_name="Активен")


    def __str__(self):
        return f"Участок {self.name} на {self.line.get_line_name_display()}"
