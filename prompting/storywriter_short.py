import openai
import prompting.prompt_text as prompt_text
import prompting.openai_model_info as openai_model_info
import tiktoken
import logging
from langchain.prompts import PromptTemplate
import time

class ShortStoryWriter:

    def __init__(self, org_key, api_key, model='gpt-3.5-turbo', lc_model='gpt-3.5-turbo-16k'):
        """
        model: base model used for shorter context requests
        lc_model: larger context model used for longer content generation requests
        """
        self.model = model
        self.lc_model = lc_model
        self.compute = []

        openai.organization = org_key
        openai.api_key = api_key

    def author(self, prompt, output_dir, n_chapters=5):
        """
        Returns an entire short novel based on a short input prompt
        """
        start = time.time()
        self.n_chapters = n_chapters
        # TODO refactor with LLMChain 

        summary = self.plot_summary(prompt)
        logging.info(summary)
        character_outline = self.character_outline(summary)
        logging.info(character_outline)
        outline = self.outline(summary, character_outline)
        logging.info(outline)
        # skipping robust outline for now
        story = self.write_novella(outline, character_outline)

        print(self.compute_costs())
        elapsed = time.time() - start
        compute_time = time.strftime('%H:%M:%S', time.gmtime(elapsed))
        print(f"wall time to compute: {compute_time}")

        if output_dir:
            with open(output_dir + 'story.txt', 'w') as file:
                file.write(story)
        return story

    def plot_summary(self, concept, iterations=3):
        """
        prompting for generation of plot summaries. 

        concept: plain text story idea roughly of the form: "A story about..."
        iterations: number of generated plot summaries. All outputs will be pruned and the best one will be selected 
        """
        prompt = prompt_text.SUMMARY.format(concept=concept, n_chapters=self.n_chapters)
        logging.debug(prompt)
        response = self.get_response(self.model, prompt, max_tokens=1200, n=iterations)
        if iterations == 1:
            return response['choices'][0]['message']['content']
        return self.reflect(response)

    def reflect(self, response):
        summaries = ''
        for i, choice in enumerate(response['choices']):
            summary = f"Summary {i+1}: {choice['message']['content']}"
            logging.debug(summary)
            summaries += summary
        
        prompt = prompt_text.SELF_REFLECTION.format(summaries=summaries)
        response = self.get_response(self.lc_model, prompt, max_tokens=8000)
        
        return response['choices'][0]['message']['content']
    
    def character_outline(self, summary):
        prompt = prompt_text.CHARACTER_CONTEXT.format(summary=summary)
        response = self.get_response(self.model, prompt, max_tokens=2048)

        return response['choices'][0]['message']['content']


    def outline(self, summary, character_context):
        prompt = prompt_text.OUTLINE.format(summary=summary, character_context=character_context)
        response = self.get_response(self.lc_model, prompt, 8000)
        return response['choices'][0]['message']['content']
    
    # TODO determine if this is at all useful
    def robust_outline(self, outline):
        prompt = prompt_text.ENRICH.format(outline=outline)
        response = self.get_response(self.lc_model, prompt, 10000)

        return response['choices'][0]['message']['content']
    
    def write_novella(self, outline, character_outline):

        full_text = ''

        for i in range(self.n_chapters):
            full_text += self.write_chapter(outline, character_outline, i+1)

        return full_text

    def write_chapter(self, outline, character_context, chapter_num):
        prompt = prompt_text.WRITE_CHAPTER.format(outline=outline, character_context=character_context, chapter_num=chapter_num)

        response = self.get_response(self.lc_model, prompt, 7000)
        return response['choices'][0]['message']['content']

    def get_response(self, model, prompt, max_tokens, temperature=1, n=1):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {'role': 'system', 'content': prompt_text.SYSTEM},
                {'role': 'user', "content": prompt},
            ],
            temperature=temperature,
            n=n,
            max_tokens=max_tokens, 
        )
        self.compute.append([response['model'], response['usage']['total_tokens']])
        return response

    def compute_costs(self):
        """returns total compute cost for """

        total_cost = 0.0
        for model, total_tokens in self.compute:
            total_cost += openai_model_info.get_call_cost(model, total_tokens)

        return f"total cost for story generation: ${total_cost}"

    def __get_max_tokens(self, messages):
        model_max = 4096
        
        input_text = ''
        for m in messages:
            input_text += m['content']

        encoding = tiktoken.encoding_for_model(self.model)
        input_tokens = len(encoding.encode(input_text)) 

        return model_max - input_tokens - 20
