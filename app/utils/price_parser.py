from bs4 import BeautifulSoup
from typing import Dict

def html_dump_to_dict(html: str) -> Dict[str, object]:
    soup = BeautifulSoup(html, "html.parser")
    result = {}

    keys = soup.find_all("span", class_="sf-dump-key")
    values = soup.find_all("span", class_="sf-dump-str") + soup.find_all("span", class_="sf-dump-num")

    for key_span, value_span in zip(keys, values):
        key = key_span.text.strip()
        value = value_span.text.strip()
        try:
            if '.' in value:
                value = float(value)
            else:
                value = int(value)
        except ValueError:
            pass
        result[key] = value

    return result
