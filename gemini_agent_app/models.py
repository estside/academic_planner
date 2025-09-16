# gemini_agent_app/models.py
from django.db import models
from django.contrib.auth.models import User
# You'll need a library like `pgvector` for this, which requires PostgreSQL
# from pgvector.django import VectorField

class DocumentChunk(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    source_file = models.CharField(max_length=255)
    # embedding = VectorField(dimensions=768) # Example for a specific model
    
    def __str__(self):
        return f"Chunk from {self.source_file}"