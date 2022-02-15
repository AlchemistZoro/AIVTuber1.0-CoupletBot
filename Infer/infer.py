import os
import sys
from pyrsistent import b
import torch
import csv
from model import  BiLSTM
from datetime import datetime
from tts import getvoice
import time

from playsound import playsound

import codecs

from torchtext.legacy.data import Field, Dataset, Example,BucketIterator,Iterator
from torchtext.vocab import Vectors

import pandas as pd

from sqlpipline import SQLpipline

a_file = open("./data/vocab.csv", "r",encoding="utf8")
reader = csv.reader(a_file)
itos = {int(rows[0]):rows[1] for rows in reader}
stoi=dict(zip(itos.values(), itos.keys()))
a_file.close()

DEVICE=torch.device('cuda' if torch.cuda.is_available() else 'cpu')
SEED=2022
torch.manual_seed(SEED)
def load_sentences(path,p0='train',p1='in'):
    path=path+p0+'/'+p1+'.txt'
    text_list=[]
    for line in codecs.open(path, 'r', 'utf-8'):
        #drop the final dimension
        line=line.split(' ')[0:-1]
        text_list.append(line)
    return text_list

root_path='./data/couplet-pro/'
para0=['train','test']
para1=['in','out']
train_in_sentences=load_sentences(root_path,'train','in')
train_out_sentences=load_sentences(root_path,'train','out')
assert len(train_in_sentences)==len(train_out_sentences)

def laod_dataset(sentence_in,sentence_out,textfield):

    len_sen=len(sentence_in)
    examples=[]
    fields = [('_in', textfield), ('_out', textfield)]
    for i in range(len_sen):
        examples.append(Example.fromlist([sentence_in[i], sentence_out[i]], fields))    
    dataset = Dataset(examples, fields)
    return dataset
TEXT=Field(sequential=True,use_vocab=True,include_lengths=True)
train_data=laod_dataset(train_in_sentences,train_out_sentences,textfield=TEXT)


BATCH_SIZE=512
vectors = Vectors(name='../data/sgns.sikuquanshu.word') 

TEXT.build_vocab(train_data,vectors=vectors)
INPUT_DIM = len(TEXT.vocab)
EMBEDDING_DIM=300
HIDDEN_DIM = 300

model=BiLSTM(
    vocab_size=INPUT_DIM,
    embedding_dim=EMBEDDING_DIM,
    hidden_dim=HIDDEN_DIM,
     ).to(DEVICE) 
model.load_state_dict(torch.load('./model/model_all.pt'))

sqlp=SQLpipline()

# text_in_list=['关注嘉然顿顿解馋','心怀不惧，方能翱翔于天际','监管如我，站尽芜杂']
# user_in_list=['wzc123','牛是是是123の徳の','正常的人类是我']
# idx=0
while 1:    

    text_in,user_name,hash_id=sqlp.get_text_in()
    # text_in=text_in_list[idx]
    # user_name=user_in_list[idx]
    # idx+=1
    if text_in !='':
        sen_list=list(text_in)
        sen_len=len(sen_list)
        sen_size=[sen_len]
        indexed = [TEXT.vocab.stoi[t] for t in sen_list]
        tensor = torch.LongTensor(indexed).to(DEVICE)              #转换为张量
        tensor = tensor.unsqueeze(1).T  
        prediction = model(tensor,sen_size)
        max_preds = prediction.argmax(dim = 2, keepdim = True)
        max_preds=max_preds.reshape(sen_len)
        sen_predict=[TEXT.vocab.itos[t] for t in max_preds]
        text_out=''.join(sen_predict)
        in_template='''{user_name}给出的上联是：\n=={text_in}=='''.format(user_name=user_name,text_in=text_in)
        out_template='''我给出的下联是：\n=={text_out}==\n===================(≧∇≦)ﾉ==================='''.format(text_out=text_out)
        voice_template='''{user_name}给出的上联是，{text_in}，我给出的下联是，{text_out},谢谢{user_name}，有人能和我一起玩真实太好了'''.format(user_name=user_name,text_in=text_in,text_out=text_out)
        print(in_template)

        getvoice(voice_template)
        playsound('result.mp3')
        os.remove('result.mp3')
        print(out_template)
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        sqlp.process_text_out(hash_id,text_out,date_time)
    time.sleep(1)




