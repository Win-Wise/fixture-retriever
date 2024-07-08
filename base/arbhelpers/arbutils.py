from unidecode import unidecode
import datetime

synonyms = {
    "w": "women"
}

bad_words = [
    "club", "deportivo", "ca", "fc", "atletico", "cd", "futebol", "clube", "ac",
    "fk", "ifk", "fb", "sk", "ff", "if", "sp", "fbc", "ii"
]


def is_valid_event(event, days_forward):
    lower_bound = datetime.datetime.now(datetime.timezone.utc)
    upper_bound = lower_bound + datetime.timedelta(days=days_forward)
    return lower_bound <= event.start_time <= upper_bound


def clean_name(name):
    name = name.lower()
    name = name.replace("[w]", "women")
    name = unidecode(name)
    tokens = name.split()
    name_string = ""

    # replace common words with synonyms and removing superfluous words
    for token in tokens:
        if token in synonyms:
            name_string += synonyms[token] + " "
        elif token in bad_words:
            continue
        else:
            name_string += token + " "
    name_string = name_string.strip()

    return name_string
