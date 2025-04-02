from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
"""
Try to use generics.ListAPIView to get sensor's data in specific time range
"""


class SensorHistoryTrendView(generics.ListAPIView):
    """
    Once we add FilterBackend, We need to mention:
    which fields we need to filter
    """
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["time"]