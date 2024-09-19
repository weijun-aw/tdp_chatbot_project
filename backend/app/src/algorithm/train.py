import json, os
from ..algorithm.nltk_utils import tokenize,stem,bag_of_words
#from nltk_utils import tokenize,stem,bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
#from model import NeuralNet
from ..algorithm.model import NeuralNet

#Read our intent json file

file_name = 'intent.json'

# Get the current directory of the script
current_dir = os.path.dirname(__file__)

# Create the full path to the JSON file
file_path = os.path.join(current_dir, file_name)

with open(file_path,'r') as f:
    intent = json.load(f)

#Create empty list to store all the words, tags and xy
all_words = []
tags = []
xy=[]
#Loop through the intents and append the words and tags to the list
for intents in intent['intents']:
    tag = intents['tag']
    tags.append(tag)
    for pattern in intents['patterns']:
        w = tokenize(pattern)
        all_words.extend(w)
        xy.append((w,tag))

#ignore punctuations
ignore_words = ['?','!','.',',']
#Stem and lower each word and remove duplicates
#Sort the words
all_words = [stem(w) for w in all_words if w not in ignore_words]
all_words = sorted(set(all_words))
#unique labels for each tag
tags = sorted(set(tags))

#Create training data
x_train = []
y_train = []
for (pattern_sentence, tag) in xy:
    bag = bag_of_words(pattern_sentence, all_words)
    x_train.append(bag)

    label = tags.index(tag)
    #Cross Entropy Loss
    y_train.append(label) 

x_train = np.array(x_train)
y_train = np.array(y_train) 

class ChatDataset(Dataset):
    def __init__(self):
        self.n_samples = len(x_train)
        self.x_data = x_train
        self.y_data = y_train

    #dataset[index]
    def __getitem__(self, index):
        return self.x_data[index], self.y_data[index]

    #dataset[idx]
    def __len__(self):
        return self.n_samples
    
#Hyperparameters
batch_size = 8
hidden_size = 8
output_size = len(tags)
input_size = len(x_train[0])
learning_rate = 0.001
num_epochs = 1000
    

dataset = ChatDataset()
train_loader = DataLoader(dataset=dataset,batch_size=batch_size,shuffle=True,num_workers=0)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNet(input_size, hidden_size, output_size)

#Loss and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for (words, labels) in train_loader:
        words = words.to(device)
        labels = labels.to(device)
        #forward pass
        outputs = model(words)
        loss = criterion(outputs, labels)
        #backward and optimizer step
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    #Print the epoch and loss every 100 epochs
    if(epoch+1)% 100 ==0:
        print(f'epoch {epoch+1}/{num_epochs}, loss={loss.item():.4f}')

print(f'final loss, loss={loss.item():.4f}')

#Create a dictionary to save the model
data ={
    "model_state": model.state_dict(),
    "input_size": input_size,
    "output_size": output_size,
    "hidden_size": hidden_size,
    "all_words": all_words,
    "tags": tags
}

#Create a file
FILE ="data.pth"
#Save the file into a pickle file
torch.save(data,FILE)
print(f'training complete. file saved to {FILE}')