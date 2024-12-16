from django.db import models
from django.utils import timezone 

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Downtime(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f"{self.equipment.name} - {self.reason}"

class Speed(models.Model):
    data = models.DateField("Дата")
    time = models.TimeField("Время")
    line = models.IntegerField(
        "Номер линии", default=0, blank=True, null=True
    )
    speed = models.IntegerField(
        "Скорость", default=0.0, blank=True, null=True
    )

    
    def __str__(self):
        return str(self.data) + " " + str(self.time)

    class Meta:
        verbose_name_plural = "Производительность линии"

class ProductOutput(models.Model):
    date = models.DateField("Дата")
    time = models.TimeField("Время")
    line = models.IntegerField(
        "Номер линии", default=0, blank=True, null=True
    )
    quantity = models.IntegerField(
        "Количество продукции", default=0, blank=True, null=True
    )

    def __str__(self):
        return f"Линия {self.line} - {self.quantity} шт. ({self.date} {self.time})"

    class Meta:
        verbose_name_plural = "Производство продукции"


from django.db import models
from datetime import datetime
from django.utils import timezone

class Table(models.Model):
    startdata = models.DateField("Дата начала простоя", default=datetime.now)  # Используем datetime.now для локальной даты
    starttime = models.TimeField("Время начала простоя", blank=True, null=True)
    prostoy = models.TimeField("Время простоя", blank=True, null=True)
    line = models.IntegerField("Номер линии", default=0, blank=True, null=True)
    uchastok = models.CharField("Где произошел простой", max_length=50, default="", blank=True, null=True)
    prichina = models.CharField("Причина", max_length=50, default="", blank=True, null=True)
    otv_pod = models.CharField("Ответственное подразделение", max_length=50, default="", blank=True, null=True)
    comment = models.CharField("Комментарий", max_length=250, default=" ", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.starttime:
            self.starttime = datetime.now().time()
        if not self.startdata:
            self.startdata = datetime.now().date()
        super(Table, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.startdata}_{self.starttime}_{self.line}_{self.id}"

    class Meta:
        verbose_name_plural = "Простои линии"

    @staticmethod
    def start_prostoy(line, uchastok="", prichina="", otv_pod="", comment=""):
        """
        Функция для начала простоя, создает запись с текущей датой и временем.
        """
        print("tut")
        table = Table(
            startdata=datetime.now().date(),
            starttime=datetime.now().time(),
            line=line,
        )
        table.save()
        return table

    @staticmethod
    def end_prostoy(line):
        """
        Функция для завершения простоя, вычисляет разницу между временем окончания и началом простоя.
        """
        # Получаем последнюю запись по линии
        last_entry = Table.objects.filter(line=line).order_by('-startdata', '-starttime').first()
        if not last_entry:
            return None  # Нет записи для данной линии
        
        # Получаем текущее время
        end_time = datetime.now()
        start_time = datetime.combine(last_entry.startdata, last_entry.starttime)

        # Вычисляем разницу во времени
        time_difference = end_time - start_time

        # Записываем время простоя в поле prostoy
        last_entry.prostoy = time_difference
        last_entry.save()
        return last_entry
