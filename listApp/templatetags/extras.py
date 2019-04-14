from django import template

register = template.Library()

@register.filter
def splitLineBreaks(value):
    return value.split('\n')

@register.filter
def splitCommas(value):
    return value.split(',')

@register.filter
def splitSemicolons(value):
    return value.split(';')

@register.filter
def splitLinks(value):
    newValue = value.replace('link:', '')
    newValue = newValue.replace(';', '')
    return newValue

@register.filter
def splitImages(value):
    newValue = value.replace('image:', '')
    newValue = newValue.replace(';', '')
    return newValue

@register.filter
def argZero(value):
    return value[0]

@register.filter
def argOne(value):
    return value[1]

@register.filter
def length(value):
    return len(value)