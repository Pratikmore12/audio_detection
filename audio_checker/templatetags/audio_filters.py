from django import template
import re

register = template.Library()

@register.filter
def format_timestamp(seconds):
    """
    Convert seconds (float) to hh:mm:ss.sss format
    """
    if seconds is None:
        return "00:00:00.000"
    
    try:
        seconds = float(seconds)
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        
        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"
    except (ValueError, TypeError):
        return "00:00:00.000" 