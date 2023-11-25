

def classify_docs(image,processor, model):
    # prepare image for the model
    encoded_inputs = processor(image, return_tensors="pt",truncation=True)

    # make sure all keys of encoded_inputs are on the same device as the model
    for k,v in encoded_inputs.items():
      encoded_inputs[k] = v.to(model.device)

    # forward pass
    outputs = model(**encoded_inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    return predicted_class_idx
    
