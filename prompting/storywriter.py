import openai
import prompting.prompts as prompts
import prompting.modelinfo as modelinfo
import tiktoken
import logging
from langchain.prompts import PromptTemplate
from prompting.story import Story
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
        self.story = None
        self.n_chapters = None

        openai.organization = org_key
        openai.api_key = api_key

    def author(self, prompt, n_chapters=5):
        """
        Returns an entire short novel based on a short input prompt
        """
        start = time.time()
        self.story = Story()
        self.n_chapters = n_chapters

        summary = self.plot_summary(prompt)
        self.story.set_character_context(self.character_outline(summary))
        self.story.set_outline(self.outline(summary))
        self.write_novella()
        self.gen_title()

        total_cost = self.compute_costs()
        elapsed = time.time() - start
        compute_time = time.strftime('%H:%M:%S', time.gmtime(elapsed))
        
        logging.debug(f"wall time to compute: {compute_time}")
        logging.debug(f"total cost for story generation: ${total_cost}")

        return self.story, total_cost, compute_time

    def plot_summary(self, concept, iterations=3):
        """
        prompting for generation of plot summaries. 

        concept: plain text story idea roughly of the form: "A story about..."
        iterations: number of generated plot summaries. All outputs will be pruned and the best one will be selected 
        """
        prompt = prompts.SUMMARY.format(concept=concept, n_chapters=self.n_chapters)
        logging.debug(prompt)
        response = self.get_response(self.model, prompt, max_tokens=1200, n=iterations)
        if iterations == 1:
            return response['choices'][0]['message']['content']
        
        summary = self.reflect(response)
        logging.debug(summary)

        return summary

    def reflect(self, response):
        summaries = ''
        for i, choice in enumerate(response['choices']):
            summary = f"Summary {i+1}: {choice['message']['content']}"
            logging.debug(summary)
            summaries += summary
        
        prompt = prompts.SELF_REFLECTION.format(summaries=summaries)
        response = self.get_response(self.lc_model, prompt, max_tokens=8000)
        
        return response['choices'][0]['message']['content']
    
    def character_outline(self, summary):
        prompt = prompts.CHARACTER_CONTEXT.format(summary=summary)
        response = self.get_response(self.model, prompt, max_tokens=2048)

        character_outline = response['choices'][0]['message']['content']
        logging.debug(character_outline)
        
        return character_outline


    def outline(self, summary):
        prompt = prompts.OUTLINE.format(summary=summary, character_context=self.story.character_context)
        response = self.get_response(self.lc_model, prompt, 8000)

        outline = response['choices'][0]['message']['content']
        logging.debug(outline)

        return outline
    
    # TODO determine if this is at all useful
    def robust_outline(self, outline):
        prompt = prompts.ENRICH.format(outline=outline)
        response = self.get_response(self.lc_model, prompt, 10000)

        return response['choices'][0]['message']['content']
    
    def write_novella(self):
        for i in range(self.n_chapters):
            cnum = i+1
            self.story.add_chapter(self.write_chapter(self.story.outline, self.story.character_context, cnum), cnum)

    def write_chapter(self, outline, character_context, chapter_num):
        prompt = prompts.WRITE_CHAPTER.format(outline=outline, character_context=character_context, chapter_num=chapter_num)

        response = self.get_response(self.lc_model, prompt, 7000)
        return response['choices'][0]['message']['content']

    def gen_title(self):
        prompt = prompts.GENERATE_TITLE.format(outline=self.story.outline)
        response = self.get_response(self.model, prompt, max_tokens=1200)

        self.story.set_title(response['choices'][0]['message']['content'])


    def get_response(self, model, prompt, max_tokens, temperature=1, n=1):
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {'role': 'system', 'content': prompts.SYSTEM},
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
            total_cost += modelinfo.get_call_cost(model, total_tokens)

        return total_cost

    def __get_max_tokens(self, messages):
        model_max = 4096
        
        input_text = ''
        for m in messages:
            input_text += m['content']

        encoding = tiktoken.encoding_for_model(self.model)
        input_tokens = len(encoding.encode(input_text)) 

        return model_max - input_tokens - 20
