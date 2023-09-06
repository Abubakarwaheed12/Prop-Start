from django import template

register = template.Library()

@register.simple_tag
def first_two_words(input_string):
    # Split the input string into words
    words = input_string.split()
    
    # Take the first two words and join them back into a single string
    result = ' '.join(words[:2])
    
    return result
