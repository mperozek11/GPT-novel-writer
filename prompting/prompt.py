class Prompt:

    
    def __init__(self, content):
        """
        Initialize the Prompt with its content.

        :param content: The content of the prompt.
        """
        self.content = content

    def __call__(self, previous_response=None):
        """
        Make the Prompt callable. This will execute the prompt and may use the previous response.

        :param previous_response: The result of the previous prompt.
        :return: User input in response to the prompt.
        """
        # Here, we're just using the previous response as a part of the prompt, but this can be adapted as needed.
        return input(f"{previous_response if previous_response else ''}{self.content}")

class PromptPipeline:
    def __init__(self, prompts=None):
        """
        Initialize the PromptPipeline with an initial list of prompts.

        :param prompts: List of initial Prompt objects.
        """
        if prompts is None:
            prompts = []
        self.prompts = prompts

    def add_prompt(self, prompt_content, index=None):
        """
        Add a new prompt to the pipeline. Optionally specify an index to insert the prompt at a specific position.

        :param prompt_content: The content of the new prompt to add.
        :param index: The position to insert the new prompt. If None, the prompt is appended to the end.
        """
        prompt = Prompt(prompt_content)
        if index is None:
            self.prompts.append(prompt)
        else:
            self.prompts.insert(index, prompt)

    def execute_pipeline(self, initial_prompt):
        """
        Execute the entire prompt pipeline.

        :param initial_prompt: The initial prompt to execute before starting the pipeline.
        :return: List of results for each prompt in the pipeline.
        """
        results = []
        
        # Execute the initial prompt.
        response = initial_prompt()

        # Execute the main pipeline.
        for prompt in self.prompts:
            response = prompt(response)
            results.append(response)

        return results

# Example Usage:
pipeline = PromptPipeline([Prompt("What's your name? "), Prompt("Thanks, {}. How old are you? ")])
pipeline.add_prompt("Nice! So, {}, where do you live? ")

initial = Prompt("Welcome to the survey! Press Enter to continue...")
responses = pipeline.execute_pipeline(initial_prompt=initial)
print(responses)
