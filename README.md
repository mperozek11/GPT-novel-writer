# GPT-reflect-writer

An experiment in LLM prompt engineering and self-reflection built specifically for novel writing. 

Self-reflection loosely inspired by [this paper](https://arxiv.org/pdf/2303.11366.pdf).

### Instructions
Run: 

`python writer.py "<your story concept here>" OPENAI_API_KEY OPENAI_ORG_KEY`

If you prefer, you can export your API key and org key as environment variables using the names:
`OPENAI_API_KEY` and `OPENAI_ORG_KEY`.

TODO
- Save story to a file 
- Genre/ 'in the style of author' support: Allows for arbitrary genre input, generates genre/ style context for writing and plot.
- Add a prompt debugger that outputs a file tracing each prompting step with input and output