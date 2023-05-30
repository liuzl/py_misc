from ctransformers import AutoModelForCausalLM
llm = AutoModelForCausalLM.from_pretrained('marella/gpt-2-ggml')
tokens = llm.tokenize('AI is going to')

for token in llm.generate(tokens):
    print(llm.detokenize(token))
