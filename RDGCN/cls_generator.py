import torch
import transformers
from transformers import BertTokenizer, BertModel
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
import time  # To measure running time
import numpy as np  # Use NumPy for faster array operations
from Param import *

# Custom Dataset class to handle text inputs
class TextDataset(Dataset):
    def __init__(self, text_list, tokenizer, max_length=512):
        self.text_list = text_list
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.text_list)

    def __getitem__(self, idx):
        text = self.text_list[idx]
        # Tokenize the text
        inputs = self.tokenizer(text, return_tensors='pt', padding='max_length', truncation=True, max_length=self.max_length)
        return {
            'input_ids': inputs['input_ids'].squeeze(0),  # Remove batch dimension
            'attention_mask': inputs['attention_mask'].squeeze(0)
        }

# Define the model with dropout and linear layer for dimensionality reduction
class BERTCLSExtractor(nn.Module):
    def __init__(self, model_name=PRETRAINED_TEXT_EMB_MODEL, output_dim=300):
        super(BERTCLSExtractor, self).__init__()
        self.bert_model = BertModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(p=0.3)
        self.out_linear_layer = nn.Linear(768, output_dim)  # Reduces 768-dim to 300-dim

    def forward(self, batch_word_list, attention_mask):
        # Forward pass through BERT
        x = self.bert_model(input_ids=batch_word_list, attention_mask=attention_mask)
        sequence_output = x[0]  # Get token embeddings
        cls_vec = sequence_output[:, 0]  # CLS token is the first token
        output = self.dropout(cls_vec)
        output = self.out_linear_layer(output)
        return output

# Function to handle batching, GPU processing, and return faster NumPy arrays
def get_cls_embeddings_in_batches(text_list, batch_size=16, output_dim=300, device='cuda', use_fp16=True):
    # Initialize tokenizer and model
    tokenizer = BertTokenizer.from_pretrained(PRETRAINED_TEXT_EMB_MODEL)
    model = BERTCLSExtractor(output_dim=output_dim)
    
    # Move the model to GPU if available
    model.to(device)
    
    # Set the model to evaluation mode (disable dropout during inference)
    model.eval()

    # Create a dataset and DataLoader for batch processing
    dataset = TextDataset(text_list, tokenizer)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

    all_cls_embeddings = []

    # Measure time
    start_time = time.time()

    # Use automatic mixed precision for faster processing
    scaler = torch.cuda.amp.GradScaler() if use_fp16 else None
    #print("Length of DataLoader and batches number:", len(dataloader), len(dataloader)//batch_size)
    total_batches = len(dataloader)
    print(f"Total number of batches: {total_batches}")

    # Loop over batches and process them on the GPU
    with torch.no_grad():  # Disable gradient computation for efficiency
        for batch_idx, batch in enumerate(dataloader, start=1):
            print(f"Processing batch {batch_idx}/{total_batches}...")

#        for batch in dataloader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            
            # Use mixed precision if enabled
            with torch.cuda.amp.autocast(enabled=use_fp16):
                # Get CLS embeddings for the current batch
                cls_embeddings = model(input_ids, attention_mask)

            # Store embeddings directly in GPU and convert to NumPy array at the end
            all_cls_embeddings.append(cls_embeddings.detach().cpu().numpy())

    # Measure time
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Time taken for embedding: {elapsed_time:.2f} seconds")

    # Concatenate all embeddings and convert to a list of lists if needed
    final_embeddings = np.concatenate(all_cls_embeddings, axis=0)  # Keep as NumPy array for efficiency
    return final_embeddings.tolist()  # Convert to list of lists at the very end

# Function that accepts a list of texts and returns the embeddings
def get_cls_embeddings(text_list, batch_size=256, output_dim=300, use_fp16=True): #16
    # Check for GPU availability
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    # Get the CLS embeddings
    embeddings = get_cls_embeddings_in_batches(text_list, batch_size=batch_size, output_dim=output_dim, device=device, use_fp16=use_fp16)
    
    return embeddings
if __name__ == "__main__":
    # Sample list of texts
    text_list = ["This is an example sentence.", "This is another example.", "Yet another example."]
    
    # Get the CLS embeddings and print the running time
    embeddings = get_cls_embeddings(text_list, batch_size=2, output_dim=300, use_fp16=True)
    
    print("CLS Embeddings (list of lists):", embeddings)

