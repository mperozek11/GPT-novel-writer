from prompting.storywriter_short import ShortStoryWriter
import logging
import os
import argparse

# logging.basicConfig(level=logging.INFO)

def setup_logging(log_level):
    logging.basicConfig(level=log_level)
    logging.info("Logging initialized at %s level", logging.getLevelName(log_level))
    
def main():

    parser = argparse.ArgumentParser(description='Generate short stories based on a prompt.')
    
    # Add command line arguments
    parser.add_argument('--prompt', default='a story about a dog who fights jesus', 
                        help='The prompt to base the story on.')
    parser.add_argument('--api_key', default=os.getenv('OPENAI_API_KEY'), 
                        help='Your OpenAI API Key.')
    parser.add_argument('--org_key', default=os.getenv('OPENAI_ORG_KEY'), 
                        help='Your organization key.')
    parser.add_argument('--log', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')

    args = parser.parse_args()

    log_level = getattr(logging, args.log.upper())
    setup_logging(log_level)

    logging.debug(args.prompt)
    logging.debug(args.org_key)
    logging.debug(args.api_key)

    writer = ShortStoryWriter(org_key=args.org_key, api_key=args.api_key)
    story = writer.author(args.prompt)
    print(story)

    return

    # old vv
    org_key = 'org-SVcbPvQFyGx47d4LxAQpHQGP'
    test_prompt = "a story about a dog who fights jesus"


if __name__ == '__main__':
    main()