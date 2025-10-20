from django import template

register = template.Library()

@register.filter
def calculate_percentage(obtained_marks, max_marks):
    try:
        return round((obtained_marks / max_marks) * 100, 2)
    except (ZeroDivisionError, TypeError):
        return 0.0



register = template.Library()

@register.filter(name='get_subjects')
def get_subjects(program):
    subject_map = {
        'FA': ['Arts', 'Humanities'],
        'FSC': ['Medical', 'Computer Science', 'Political Science'],
        'BS': ['Computer Science', 'BBA Hons', 'Political Science', 'English']
    }
    return subject_map.get(program, [])