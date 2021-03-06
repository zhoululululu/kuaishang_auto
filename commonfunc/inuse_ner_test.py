import requests
import codecs
import logging
from tqdm import tqdm

def ner_predict(utterance, model_name='gynaecology', url='http://192.168.26.105:32060/ner/v1'):
    params = {
        'utterance': utterance,
        'model_name': model_name
    }
    try:
        ner = requests.get(url, params=params).json()
        if ner['code'] != 200:
            raise Exception(ner['error'])
        elif ner['code'] == 200:
            return ner['data']
    except NameError as e:
        logging.error('ner NameError: {}'.format(e))
        raise Exception(e)
    except Exception as e:
        logging.error('ner error: {}'.format(e))
        raise Exception(e)


tags = [tag.strip() for tag in codecs.open("D:\\workspace\\kuaishang_auto\\testdata\\apidata\\ner\\gynaecology\\tag.txt", encoding="utf-8")]
# print(tags)

test_corpus_f = codecs.open("D:\\workspace\\kuaishang_auto\\testdata\\apidata\\ner\\gynaecology\\bio_char.txt",
                            encoding="utf-8")

sent = []
bio = []
bios = []
bio_s = []
for line in tqdm(test_corpus_f.readlines()):
    if len(line.strip()) == 0:
        sentence = "".join(sent)
        bio_ = ner_predict(sentence)["bio"]
        # print(sentence)
        # print(bio_)
        # print(bio)
        bios.extend(bio)
        bio_s.extend(bio_)
        # print("-" * 100)
        bio = []
        sent = []
    else:
        line = line.strip()
        sent.append(line.split("\t\t")[0])
        bio.append(line.split("\t\t")[1])
import pandas as pd
print(len(bios),len(bio_s))
df_result = pd.DataFrame({"人工": bios,"预测": bio_s})
df_result.to_csv("bios.csv", index=False, encoding="utf-8")
