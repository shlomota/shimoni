import requests
import pandas as pd

def get_source(text, thresh=40):
    payload = {'editDistance': "2", 'wordSpan': "3", 'windowSize': "3", 'text': text}
    r = requests.post('https://rwfs.herokuapp.com/search', json=payload)
    status = r.status_code
    result = r.json()
    df = pd.DataFrame(result["results"])
    df = df[~df.document.str.contains("Yalkut_Shimoni")]
    df["score"] = (df["count"] * 100 / df["words"].apply(len)).round()
    row = df.iloc[0]
    cls = -1
    if row.score < thresh:
        cls = -2
    elif "mishnah" in row.document or "tosefta" in row.document:
        cls = 0
    elif "Sifrei" in row.document or "Sifra" in row.document or "mechilta" in row.document:
        cls = 1
    elif "yerushalmi" in row.document:
        cls = 2
    elif "bavli" in row.document:
        cls = 3
    elif "Rabbah" in row.document:
        cls = 4
    elif "Tanchuma" in row.document:
        cls = 5
    return [cls, row.document, row.score, row.documentContent]

from preprocess_style import preprocess_single_file
from tqdm import tqdm
if __name__ == "__main__":
    chunks = preprocess_single_file(r"C:\Users\soki\PycharmProjects\tanna\shimoni_inference\shimoni.txt", do_original_paragraphs=True)
    print(len(chunks))
    df = pd.DataFrame(columns=["text", "cls", "doc", "score", "doc_text"])
    for chunk in tqdm(chunks):
        res = get_source(chunk)
        df.loc[len(df)] = [chunk, *res]

    a = 5
    # text = "בראשית ברא אלהים את השמים ואת הארץ"
    # payload = {'editDistance': "2", 'wordSpan': "3", 'windowSize': "3", 'text': text}
    # r = requests.post('https://rwfs.herokuapp.com/search', json=payload)
    # status = r.status_code
    # result = r.json()
    # df = pd.DataFrame(result["results"])
    # df["score"] = (df["count"] * 100 / df["words"].apply(len)).round()
a = 5


# ngramsCount = searchResponse.words.length;
# searchResponse.results.forEach(function (item, index) {
# $('#docs > tbody:last-child').append('<tr cls="clickable-row" id="res_' + index + '"><td>' + item.document + '</td><td>' + Math.round(item.count * 100 / ngramsCount) + '%</td></tr>');
# // console.log(item, index);
# });