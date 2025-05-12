from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

from abc import ABC, abstractmethod


class AutoCompleteModel(ABC):
    def __init__(self, model_name):
        self.model_name = model_name
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    @abstractmethod
    def generate_sentences(self, input_sentence, num_sentences=5):
        pass


class aragpt2_baseModel(AutoCompleteModel):
    def __init__(self, model_name="./aragpt2_finetuned/checkpoint-14388"):
        super().__init__(model_name)

    def generate_sentences(self, input_sentence, num_sentences=5):

        if not input_sentence:
            return []

        input_ids = self.tokenizer.encode(input_sentence, return_tensors="pt")
        input_length = input_ids.shape[1]

        with torch.no_grad():
            output_ids = self.model.generate(
                input_ids,
                max_length=input_length + 10,  # Allow a few tokens to form one word
                num_return_sequences=num_sentences,
                do_sample=True,
                top_k=50,
                top_p=0.95,
                temperature=1.0,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        predictions = set([])

        for output_id in output_ids:
        # Decode the full output      
            generated_text =  self.tokenizer.decode(output_id, skip_special_tokens=True).strip()

            # Cut off at one word after the input
            new_part = generated_text[len(input_sentence):].strip()
            next_word = new_part.split()[0:10] if new_part else ""

            full_sentence = input_sentence.strip() + " " + " ".join(next_word)

            predictions.add(full_sentence)
        
        return list(predictions)
    
