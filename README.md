# GPT-novel-writer

An experiment in LLM prompt engineering and self-reflection built specifically for novel writing. 

Self-reflection loosely inspired by [this paper](https://arxiv.org/pdf/2303.11366.pdf).

### Instructions
Run: 

`python writer.py "<your story concept here>" --api_key <your api key> --org_key <your org key> --output_dir <path to output directory>`

If you prefer, you can export your API key and org key as environment variables using the names:
`OPENAI_API_KEY` and `OPENAI_ORG_KEY`.

### TODO
- Add requirements.txt 
- Genre/ 'in the style of author' support: Allows for arbitrary genre input, generates genre/ style context for writing and plot.
- Add a prompt debugger that outputs a file tracing each prompting step with input and output

### Known bugs:
- The OpenAi API connection will occasionally timeout (read timeout=600). It is possible that this can be improved here, but it appears to be linked to OpenAi servers and may be unavoidable
