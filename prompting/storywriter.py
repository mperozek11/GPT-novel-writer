import os
import openai
import numpy as np
import tiktoken
import logging

class StoryWriter:

    JSON_FORMAT_PROMT = """
        The output should be formatted in json as a list of chapters like so:
        {
        "chapters": [
            {
                "chapter_number": 1,
                "title": "chapter 1 title",
                "plot_points": [
                    "plot point 1",
                    "plot point 2",
                    ...
                    "final plot point"
                    ]
            },
            {
                "chapter_number": 2,
                "title": "chapter 2 title",
                "plot_points": [
                    "plot point 1",
                    "plot point 2",
                    ...
                    "final plot point"
                    ]
            },
            
            ...
            
            {
                "chapter_number": final chapter number,
                "title": "chapter title",
                "plot_points": [
                    "plot point 1",
                    "plot point 2",
                    ...
                    "final plot point"
                    ]
            }
        }
        """
    
    FORMAT_PROMT = """The outline should be formatted as lists of plot points separated into chapters. Plot points should be extremely detailed, and should provide a thorough framework for the plot. The output should be formatted as a list of chapters with lists of extremely detailed plot points in each chapter."""

    def __init__(self, model='gpt-3.5-turbo'):

        self.MODEL = model

        openai.organization = 'org-SVcbPvQFyGx47d4LxAQpHQGP'
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def author(self, prompt):
        summary = self.plot_summary(prompt, 3)

        character_outine = self.character_outline(summary)
        return summary, character_outine



    def plot_summary(self, prompt, iterations=1):
        """
        prompting for generation of plot summaries. 

        prompt: plain text story idea roughly of the form: "A story about..."
        iterations: number of generated plot summaries. All outputs will be pruned and the best one will be selected 
        """
        full_prompt = f"Write me a detailed plot summary for the following short story idea: {prompt}"
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
        
        all_summaries = ""
        for i, choice in enumerate(response['choices']):
            summary = f"Summary {i+1}: {choice['message']['content']}"
            logging.debug(summary)
            all_summaries += summary

        pruning_prompt = f"The following is a list of attempts at plot summaries for the same story. Please choose the best plot summary and feel free to enrich it with elements from the other summaries. Your response should include only the best summary \n{all_summaries}"
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": pruning_prompt},
                ],
            temperature=1,
            max_tokens=2048, 
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


    def outline(self, outline):
        full_prompt = f"{outline} {self.FORMAT_PROMT}"
        # print(full_prompt)


        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": full_prompt},
            ],
            temperature=1,
            max_tokens=2048, 
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
            model=self.MODEL,
            messages=messages,
            temperature=1,
            max_tokens=self.__get_max_tokens(messages), 
        )
        return response['choices'][0]['message']['content']
    
    def write_chapter(self, outline, chapter_num):
        # probably want to switch to longer context model here
        prompt = f'Write the entirety of chapter {chapter_num} in great detail as if this were the final copy of the novella. Try to add details like foreshadowing and use rich, descriptive language.'

        messages=[
                {'role': 'system', 'content': 'You are a helpful erotic novel writing assistant.'},
                {'role': 'user', "content": outline},
                {'role': 'user', "content": prompt},
            ]
        response = openai.ChatCompletion.create(
            model=self.MODEL,
            messages=messages,
            temperature=1,
            max_tokens=self.__get_max_tokens(messages), 
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
