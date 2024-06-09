import torch
from transformers import BertForMaskedLM, BertTokenizer

class BertModel:
    def __init__(self, model_path, device):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertForMaskedLM.from_pretrained('bert-base-uncased')
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device(device)))
        self.model.to(device)
        self.model.eval()
        self.device = device

    def predict(self, input_text):
        # Tokenize the input text
        inputs = self.tokenizer.encode_plus(input_text, return_tensors='pt')
        input_ids = inputs['input_ids'].to(self.device)
        attention_mask = inputs['attention_mask'].to(self.device)
        
        # Find the position of the [MASK] token
        mask_token_index = torch.where(input_ids == self.tokenizer.mask_token_id)[1]
        
        # Make predictions
        with torch.no_grad():
            outputs = self.model(input_ids=input_ids, attention_mask=attention_mask)
        
        # Get the predicted token ids for the [MASK] position
        logits = outputs.logits
        mask_token_logits = logits[0, mask_token_index, :]
        predicted_token_id = torch.argmax(mask_token_logits, dim=-1)
        
        # Decode the predicted token id
        predicted_token = self.tokenizer.decode(predicted_token_id)
        
        return predicted_token
