# coding: utf-8

from transformers import AutoTokenizer

TOKENIZER_CBERT = AutoTokenizer.from_pretrained("camembert-base", use_fast=True)
TOKENIZER_FBERT = AutoTokenizer.from_pretrained("flaubert/flaubert_base_cased", use_fast=True)

def dice_coefficient(a, b, tokenizer):
    """
        Calcule le coefficient de DICE entre deux chaînes de caractères
        en utilisant les subunits générées par les Tokenizers.    
    """
    a = str(a)
    b = str(b)
    # Check if string is empty or contains only one character
    if not len(a) or not len(b): return 0.0
    if len(a) == 1:  a=a+u'.'
    if len(b) == 1:  b=b+u'.'
        
    # Get subunits generated with tokenizer
    input_ids = tokenizer.batch_encode_plus([a,b], return_token_type_ids=False, return_attention_mask=False, add_special_tokens=False)["input_ids"]
    a_bigram_list=tokenizer.convert_ids_to_tokens(input_ids[0])
    b_bigram_list=tokenizer.convert_ids_to_tokens(input_ids[1])

    # Calculate DICE coefficient
    a_bigrams = set(a_bigram_list)
    b_bigrams = set(b_bigram_list)
    overlap = len(a_bigrams & b_bigrams)
    dice_coeff = overlap * 2.0/(len(a_bigrams) + len(b_bigrams))
    
    return round(dice_coeff,3)


def dice_su_coefficient(a, b, tokenizer):
    """
        Calcule le coefficient de DICE entre deux chaînes de caractères
        en utilisant les subunits générées par les Tokenizers.    
    """
    a = str(a)
    b = str(b)
    # Check if string is empty or contains only one character
    if not len(a) or not len(b): return 0.0
    if len(a) == 1:  a=a+u'.'
    if len(b) == 1:  b=b+u'.'
        
    # Get subunits generated with tokenizer
    input_ids = tokenizer.batch_encode_plus([a,b], return_token_type_ids=False, return_attention_mask=False, add_special_tokens=False)["input_ids"]
    a_bigram_list=tokenizer.convert_ids_to_tokens(input_ids[0])

    b_bigram_list=tokenizer.convert_ids_to_tokens(input_ids[1])
    print(a_bigram_list, b_bigram_list, "\n")
    # Calculate DICE coefficient
    a_bigrams = set(a_bigram_list) 
    b_bigrams = set(b_bigram_list) 

    overlap = sum(map(len, list(set(a_bigrams & b_bigrams))))
    dice_coeff = overlap * 2.0/(sum(map(len, list(a_bigrams))) + sum(map(len, list(b_bigrams))))
    
    return round(dice_coeff,3)


if __name__=="__main__":
    targets = "discriminatoire, contradictoires, contraignants, néfastes, monotone".split(", ")
    source = "discriminatoires"

    print(f"Computing Dice and Dice-SU coefficients between the word {source} and the words {targets}")

    dice_cbert = []
    dice_su_cbert = []
    dice_fbert = []
    dice_su_fbert = []
    for word in targets:
        dice_cbert.append(dice_coefficient(source, word, TOKENIZER_CBERT))
        dice_su_cbert.append(dice_su_coefficient(source, word, TOKENIZER_CBERT))

        dice_fbert.append(dice_coefficient(source, word, TOKENIZER_FBERT))
        dice_su_fbert.append(dice_su_coefficient(source, word, TOKENIZER_FBERT))
    
    print("CamemBERT")
    print("SOURCE:", source)
    print("DICE:", [(word,dice) for (word,dice) in zip(targets, dice_cbert)])
    print("DICE-SU:", [(word,dice) for (word,dice) in zip(targets, dice_su_cbert)])
    print("DICE:", sum(dice_cbert)/len(dice_cbert), "\nDICE-SU:", sum(dice_su_cbert)/len(dice_su_cbert))

    print("FlauBERT")
    print(dice_fbert)
    print(dice_su_fbert)
    print("DICE:", sum(dice_fbert)/len(dice_fbert), "\nDICE-SU:", sum(dice_su_fbert)/len(dice_su_fbert))