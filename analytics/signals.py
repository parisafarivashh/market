from django.dispatch import Signal


activity_signals = Signal(['sender', 'instance', 'activity_type'])

