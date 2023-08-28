import json, numpy
from transformers import BertTokenizer, BertModel
import torch
import torch.nn as nn
model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model.to(device)
from transformers import BertModel
import torch.nn as nn

import torch
import torch.nn as nn
from transformers import BertModel, BertTokenizer
import json

class DimensionalityReducer(nn.Module):
    def __init__(self, input_dim=768, output_dim=300):
        super(DimensionalityReducer, self).__init__()
        self.linear = nn.Linear(input_dim, output_dim)

    def forward(self, embeddings):
        return self.linear(embeddings)

# Instantiate the tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Instantiate the reducer
reducer = DimensionalityReducer().to(device)
data_sentence={}
with open('data.json', 'r') as f:
    for line_number, line in enumerate(f, start=1):
        if line_number >= 1:
            data = json.loads(line)
            list_words = data["token"]
            sentence = " ".join(list_words)
            tokens = tokenizer.tokenize(sentence)
            tokens_ids = tokenizer.convert_tokens_to_ids(tokens)
            tokens_ids = [tokenizer.cls_token_id] + tokens_ids + [tokenizer.sep_token_id]
            input_ids = torch.tensor(tokens_ids).unsqueeze(0).to(device)

            with torch.no_grad():
                outputs = model(input_ids)
                last_hidden_state = outputs.last_hidden_state
                word_embeddings = last_hidden_state.squeeze(0)

                for i, token in enumerate(tokens):
                    word_embedding_300 = reducer(word_embeddings[i])  # Reduce the dimensionality

                    print(word_embedding_300.shape)
                    data_sentence[token] = word_embedding_300.numpy().tolist()

                with open("output.json", "a") as file:
                    json.dump(data_sentence, file)
                    file.write("\n")

        print("————————————%srow——————————————" % line_number, round(line_number / 804414, 5))