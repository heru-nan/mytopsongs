from django.db import models

class Node(models.Model):
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    message = models.CharField(max_length=100)
    pub_date = models.DateTimeField('date published')

    def get_token_message(self):
        return {
            "token": self.token,
            "message": self.message
        }
    
    
