from django import template
 
register = template.Library()

@register.filter(name='Censor')

def censor(text):
    censor_words = ['ipsum', 'lorem', 'python']
    text1 = text.split()
    punctuation = ',.!?:;-'
    for word in text1:
        if word[-1] in punctuation:
            word = word[:-1]
        if word.lower() in censor_words:
            text = text.replace(word, word[0] + ('*' * (len(word) - 1)))
    return text