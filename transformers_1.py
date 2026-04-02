from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-hf", dtype="auto", device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf")

model_inputs = tokenizer(
    ["The secret to baking a good cake is "], return_tensors="pt"
).to(model.device)
output = model.generate(**model_inputs, max_new_tokens=20)

print(tokenizer.batch_decode(output, skip_special_tokens=True))
