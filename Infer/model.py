from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from torch import nn 
class BiLSTM(nn.Module):
    #定义模型中使用的所有层
    def __init__(self, vocab_size, embedding_dim=100, hidden_dim=120,):
        #构造函数
        super().__init__()
        #embeddding层
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        #lstm层
        self.lstm = nn.LSTM(embedding_dim, 
                           hidden_dim,
                           num_layers=1,
                           bidirectional=True, 

                           batch_first=True)
        self.fc = nn.Linear(hidden_dim*2, vocab_size)

    def forward(self, text,text_lengths):
        embedded=self.embedding(text) #添加了padding的embedding结果

        packed_embedded=pack_padded_sequence(embedded,text_lengths,batch_first=True,enforce_sorted=False)
        packed_output,_=self.lstm(packed_embedded) #没有padding的输出
        output,output_lengths=pad_packed_sequence(packed_output, batch_first=True) #返回输出，和没有padding的

        output=self.fc(output)
        return output
