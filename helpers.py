import config

def titlecase(tuple):
    # Converts a tuple of strings to titlecasing (Each string should be 1 word)
    # e.g. hand of wisdom and action --> Hand of Wisdom and Action
    tuple = [x.lower() for x in tuple] # Convert to list so we can do reassignment
    for i in range(len(tuple)):
        if i == 0 or tuple[i] not in config.excluded_titlecase_words:
            tuple[i] = tuple[i][0].upper()+tuple[i][1:]
        else:
            continue
    return " ".join(tuple)
