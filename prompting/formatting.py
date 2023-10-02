import os
from fpdf import FPDF
from prompting.prompts import CREDIT

class StoryFormatter:

    def __init__(self):
        self.story = None
        self.path = None

    def write_to_file(self, story, path, total_cost, time, filetype='pdf'):
        self.story = story
        self.path = path
        self.total_cost = total_cost
        self.time = time

        if filetype == 'pdf':
            self.format_pdf()
        if filetype == 'txt':
            self.format_txt()
    
    def format_pdf(self):
        pdf = PDF(self.story.title, self.total_cost, self.time)
        pdf.add_page()

        pdf.disclaimer()
        for chapter, num in self.story.chapters:
            pdf.chapter_title(str(num))
            pdf.chapter_body(chapter)

        pdf_filename = f"{self.story.title}.pdf"
        pdf.output(os.path.join(self.path, pdf_filename))

    def format_txt(self):
        with open(os.path.join(self.path, f"{self.story.title}.txt"), 'w') as file:
            file.write(f"{CREDIT}\n\n\n\n{self.story.get_plaintext()}")




class PDF(FPDF):
    def __init__(self, book_title, total_cost, time):
        super().__init__()
        self.book_title = book_title
        self.total_cost = total_cost
        self.time = time
        self.add_font('DejaVu', '', 'DejaVuSerifCondensed.ttf', uni=True)

    def header(self):
        # self.add_font('DejaVu', '', 'DejaVuSerifCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 12)  
        self.cell(0, 10, self.book_title, 0, 1, 'C')

    def chapter_title(self, title):
        # self.add_font('DejaVu', '', 'DejaVuSerifCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14) 
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def disclaimer(self):
        # self.add_font('DejaVu', '', 'DejaVuSerifCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 10) 
        self.multi_cell(0, 10, CREDIT)
        self.ln(50)
        self.set_font('DejaVu', '', 20)
        self.cell(0, 10, self.book_title, 0, 1, 'C')
        self.ln(90)
        self.set_font('DejaVu', '', 14)
        self.cell(0, 10, f"total cost: ${round(self.total_cost, 2)}", 0, 1, 'L')
        self.cell(0, 10, f"generation time: {self.time}", 0, 1, 'L')
        self.add_page()


    def chapter_body(self, body):
        # self.add_font('DejaVu', '', 'DejaVuSerifCondensed.ttf', uni=True)
        self.set_font('DejaVu', '', 14) 
        self.multi_cell(0, 10, body)
        self.ln()

