from rest_framework import serializers

from .models import FrequentQuestion


class FrequentQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FrequentQuestion
        fields = (
            'subject',
            'subject2',
            'question',
            'answer',
        )