from django.db import models

# Create your models here.

class WhatsappMessage(models.Model):
    STATUS = (("pending", "Pending"),
              ("escalated", "Escalated"),
              ("completed", "Completed")
              )
    
    name = models.CharField(max_length=300)
    issue = models.TextField()
    image_url1 = models.URLField()
    image_url2 = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=300, default="pending", choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self) -> str:
        return self.issue