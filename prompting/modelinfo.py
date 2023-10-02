import logging

# Note: Pricing as of 8/29/23
# Snapshots need to be regularly as they 
# Open issue on openai GH to add cost info to API: https://github.com/openai/openai-python/issues/448

cost_per_1k_tokens = {
    'gpt-3.5-turbo' : 0.0015,
    'gpt-3.5-turbo-0613' : 0.0015,
    'gpt-3.5-turbo-16k' : 0.003,
    'gpt-3.5-turbo-16k-0613' : 0.003,
    'gpt-4' : 0.03,
    'gpt-4-0613' : 0.03,
    'gpt-4-32k' : 0.06,
    'gpt-4-32k-0613' : 0.06
}

def get_call_cost(model, total_tokens):
    try:
        return (cost_per_1k_tokens[model] / 1000) * total_tokens
    except:
        return (infer_model_cost() / 1000) * total_tokens

def infer_model_cost(model):
    # low-effort inference by trying to throw-away snapshot version. Should work unless openai changes model naming
    model_guess = ''.join(model.split('-')[:-2])
    logging.warn(f"Could not determine model version pricing. Inferred model: {model_guess}")

    try:
        cost = cost_per_1k_tokens[model_guess]
        cost_per_1k_tokens[model] = cost
    except:
        cost = 0.002 # last ditch heuristic
    
    return cost