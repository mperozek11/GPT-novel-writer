import os
import openai
import numpy as np
import tiktoken
import logging

class ShortStoryWriter:
    
    FORMAT_PROMT = """The outline should be formatted as lists of plot points separated into chapters. 
    Plot points should be extremely detailed, and should provide a thorough framework for the plot. 
    The output should be formatted as a list of chapters with bulleted lists of extremely detailed plot points in each chapter. 
    The outline should invent events to fill out the narative.""".strip()

    # the tagging is not quite working as expected. This will likely need to be separated out into another api call to go in and edit the finalized outline
    EXPLICIT_PROMPT = """Please make sure add a [CONTENT] tag around any outline bullet points with sexual encounters. And tastefully summarize the plot point"""
    TAG_IGNORE_PROMPT = """Please do not complete the writing for any of the explicit scenes marked with a [CONTENT] tag. Make sure to leave the [CONTENT] bulllet point in the text output for plot coherence."""
    # === FUTURE PROMPTING ===

    def __init__(self, model='gpt-3.5-turbo', lc_model='gpt-3.5-turbo-16k'):
        """
        model: base model used for shorter context requests
        lc_model: larger context model used for longer content generation requests
        """
        self.MODEL = model
        self.lc_model = lc_model

        openai.organization = 'org-SVcbPvQFyGx47d4LxAQpHQGP'
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def author(self, prompt, chapters=None, explicit_tag=True):
        self.explicit_tag = explicit_tag

        summary = self.plot_summary(prompt, 3)
        character_outline = self.character_outline(summary)
        logging.info(character_outline)
        outline = self.outline(summary, character_outline)
        logging.info(outline)
        # skipping robust outline for now
        story = self.write_novella(outline, character_outline)

        return story



    def plot_summary(self, prompt, iterations=3, scenes=5):
        """
        prompting for generation of plot summaries. 

        prompt: plain text story idea roughly of the form: "A story about..."
        iterations: number of generated plot summaries. All outputs will be pruned and the best one will be selected 
        """
        self.scences = scenes
        full_prompt = f"Write me a detailed plot summary for the following short story idea: {prompt}. This is a short story and should only contain {scenes} chapters"
        logging.debug(f'beginning {iterations} summary generation(s) on the following prompt: {full_prompt}')

        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": full_prompt},
            ],
            temperature=1,
            n=iterations,
            max_tokens=1024, 
        )    
        if iterations == 1:
            return response['choices'][0]['message']['content']
        
        return self.prune(response)

    def prune(self, response):
        
        all_summaries = ''
        for i, choice in enumerate(response['choices']):
            summary = f"Summary {i+1}: {choice['message']['content']}"
            logging.debug(summary)
            all_summaries += summary

        pruning_prompt = f"The following is a list of attempts at plot summaries for the same story. Please choose the best plot summary and feel free to enrich it with elements from the other summaries. Your response should include only the best summary \n{all_summaries}"
        response = openai.ChatCompletion.create(
            model=self.lc_model,
            messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": pruning_prompt},
                ],
            temperature=1,
            max_tokens=8000, 
        )
        
        return response['choices'][0]['message']['content']
    
    def character_outline(self, summary):

        character_prompt = f"The following is a summary for an erotic novella: {summary}. Please write interesting and rich backgrounds on each of the main characters (who are they, what do they want, what are their challenges, etc.). The backgrounds should be relevant to the plot summary, and should set up meaningful interactions between characters. Your response should contain only the character profiles and no additional text."
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": character_prompt},
                ],
            temperature=1,
            max_tokens=2048, 
        )

        return response['choices'][0]['message']['content']


    def outline(self, outline, character_context):
        full_prompt = f"{outline} {self.FORMAT_PROMT}. Keep in mind the following details about the main characters: {character_context}"
        if self.explicit_tag:
            full_prompt += self.EXPLICIT_PROMPT

        response = openai.ChatCompletion.create(
            model=self.lc_model,
            messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": full_prompt},
            ],
            temperature=1,
            max_tokens=8000, 
        )
        return response['choices'][0]['message']['content']
        
    def robust_outline(self, outline):
        prompt = """Given the above outline, enrich the outline, adding minute plot point details. Aim for 10-20 bullet points per chapter"""

        messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": outline},
                {'role': 'user', "content": prompt},
            ]
        response = openai.ChatCompletion.create(
            model=self.lc_model,
            messages=messages,
            temperature=1,
            max_tokens=10000, 
        )
        return response['choices'][0]['message']['content']
    
    def write_novella(self, outline, character_outline):

        full_text = ''

        for i in range(self.scences):
            full_text += self.write_chapter(outline, character_outline, i+1)

        return full_text

    def write_chapter(self, outline, character_outline, chapter_num):
        # probably want to switch to longer context model here
        prompt = f'Write the entirety of chapter {chapter_num} in great detail as if this were the final copy of the novella. Try to add details like foreshadowing and use rich, descriptive language.'
        if self.explicit_tag:
            prompt += self.TAG_IGNORE_PROMPT

        messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": outline},
                {'role': 'user', "content": f'here are some details about the important characters: {character_outline}'},
                {'role': 'user', "content": prompt},
            ]
        response = openai.ChatCompletion.create(
            model=self.lc_model,
            messages=messages,
            temperature=1,
            max_tokens=7000, 
        )
        return response['choices'][0]['message']['content']


    def __get_max_tokens(self, messages):
        model_max = 4096
        
        input_text = ''
        for m in messages:
            input_text += m['content']

        encoding = tiktoken.encoding_for_model(self.MODEL)
        input_tokens = len(encoding.encode(input_text)) 

        return model_max - input_tokens - 20
