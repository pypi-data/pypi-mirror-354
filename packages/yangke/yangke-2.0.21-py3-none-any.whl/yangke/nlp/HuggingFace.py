from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification

checkpoint="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
tokenizer=AutoTokenizer.from_pretrained(checkpoint)

raw_input = [
    "I've been waiting for a this course my whole life.",
    "I hate this so much!"
]

# padding=True, 是否需要将长度补齐成一样的
# truncation=True, 截断，限制最大长度，单独设置无效，很多模型的输入长度上限是512
# return_tensors="pt"，指底层用pytorch
inputs = tokenizer(raw_input,padding=True, truncation=True, return_tensors="pt")

decoder_input_id = inputs["input_ids"][1]
decode_input = tokenizer.decode(decoder_input_id)

print(f"{inputs=}")
print(f"{decode_input=}")

# model = AutoModel.from_pretrained(checkpoint)
#
# print(f"{model=}")
#
# outputs = model(**inputs)
# print(f"{outputs.last_hidden_state.shape=}")

model = AutoModelForSequenceClassification.from_pretrained(checkpoint)