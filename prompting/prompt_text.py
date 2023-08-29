from langchain.prompts import PromptTemplate
# ==================
# === Plain text ===
# ==================

SYSTEM = "You are a creative and original novel writer."

DIALOGUE = "When writing, be sure to include some dialogue."

# =================
# === Templates ===
# =================

SUMMARY = PromptTemplate.from_template("Write me a detailed plot summary for the following short story idea: {concept}. This is a short story and should only contain {n_chapters} chapters.")

CHARACTER_CONTEXT = PromptTemplate.from_template("The following is a summary for a short novel: {summary}. Please write interesting and rich backgrounds on each of the main characters (who are they, where do they come from, what do they want, what are their challenges, etc.) The backgrounds should be relevant to the plot summary and should set up meaningful interactions between characters. Your response should contain only the character profiles and no additional text.")

SELF_REFLECTION = PromptTemplate.from_template("""The following is a list of attempts at plot summaries for the same story. 
Please choose the best plot summary and feel free to enrich it with elements from the other summaries. 
Your response should include only the best summary {summaries}""".strip())

OUTLINE = PromptTemplate.from_template("""The following is a summary for a short novel: {summary} Please write me a plot outline for the summary. 
The outline should be formatted as lists of plot points separated into chapters. 
Plot points should be extremely detailed, and should provide a thorough framework for the plot. 
The output should be formatted as a list of chapters with bulleted lists of extremely detailed plot points in each chapter. 
The outline should invent events to fill out the narative. Keep in mind the following details about the main characters: {character_context}""".strip())

ENRICH = "{outline}\nGiven the above outline, enrich the outline, adding minute plot point details. Aim for 10-20 bullet points per chapter."

WRITE_CHAPTER = PromptTemplate.from_template("""The following is an outline for a short story: {outline}
                                            Here are some details about the main characters to keep in mind: {character_context}
                                            Write the entirety of chapter {chapter_num} in great detail as if this were the final copy of the novella. 
                                            Try to add small details about the scene and use rich, descriptive language.""".strip())
