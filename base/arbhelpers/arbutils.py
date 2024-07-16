from unidecode import unidecode
from datetime import datetime, timezone, timedelta
import boto3
import json

ai_client = boto3.client("bedrock-runtime", region_name="us-east-1")
model_id = "amazon.titan-embed-text-v2:0"

synonyms = {
    "w": "women",
    "(women)": "women",
    "[w]": "women"
}

bad_words = [
    "club", "deportivo", "ca", "fc", "atletico", "cd", "futebol", "clube", "ac",
    "fk", "ifk", "fb", "sk", "ff", "if", "sp", "fbc", "ii"
]


def get_embedding(event):
    e_dict = event.to_dict()
    request = json.dumps({
        "inputText": e_dict['text'],
        "dimensions": 256
    })
    response = ai_client.invoke_model(modelId=model_id, body=request)
    model_response = json.loads(response["body"].read())
    return model_response["embedding"]


def next_n_days(n):
    now_utc = datetime.now(timezone.utc)
    i = 0
    while i < n:
        yield now_utc
        now_utc += timedelta(days=1)
        i += 1


def is_valid_event(event, days_forward):
    lower_bound = datetime.now(timezone.utc)
    upper_bound = lower_bound + timedelta(days=days_forward)
    return lower_bound <= event.start_time <= upper_bound


def clean_name(name):
    name = name.lower()
    name = unidecode(name)
    tokens = name.split()
    name_string = ""

    # replace common words with synonyms and removing superfluous words
    for token in tokens:
        token = token.strip()
        if token in synonyms:
            name_string += synonyms[token] + " "
        elif token in bad_words:
            continue
        else:
            name_string += token + " "
    name_string = name_string.strip()

    return name_string
