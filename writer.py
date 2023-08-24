from prompting.storywriter_short import ShortStoryWriter
import logging

logging.basicConfig(level=logging.DEBUG)

def main():
    test_prompt = """An erotic short love story titled 'Ink and Indulgence' where a talented tattoo artist named Zach forms an intimate connection with a client named Claire. Claire is a powerful buisness woman who insists on keeping all of her tattoos tastefully out of sight for profesionalism. During the first tattoo session, Claire and Zach start to flirt and the sexual tension is palpable. During the second session, the two have an erotic encounter involving the tattoo gun."""
    writer = ShortStoryWriter()

    story = writer.author(test_prompt)

    print(story)




if __name__ == '__main__':
    main()