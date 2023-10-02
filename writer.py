from prompting.storywriter import ShortStoryWriter
from prompting.formatting import StoryFormatter

import logging
import os
import argparse


def setup_logging(log_level):
    logging.basicConfig(level=log_level)
    logging.info("Logging initialized at %s level", logging.getLevelName(log_level))
    
def main():
    parser = argparse.ArgumentParser(description='Generate short stories based on a prompt.')
    
    parser.add_argument('--prompt', default='A poodle fights Elon Musk in his towns annual charity boxing match')
    parser.add_argument('--api_key', default=os.getenv('OPENAI_API_KEY'), 
                        help='Your OpenAI API Key.')
    parser.add_argument('--org_key', default=os.getenv('OPENAI_ORG_KEY'), 
                        help='Your organization key.')
    parser.add_argument('--n_chapters', default=5, choices= list(range(1,31)),
                        help='Number of desired chapters in story. [1-30]')
    parser.add_argument('--output_dir', default=None, 
                        help='path to output directory for finished story.')
    parser.add_argument('--filetype', default='pdf', choices=['pdf', 'txt'], 
                        help='Output file format')
    parser.add_argument('--log', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')

    args = parser.parse_args()

    log_level = getattr(logging, args.log.upper())
    setup_logging(log_level)
    logging.debug(args.prompt)
    logging.debug(args.org_key)
    logging.debug(args.api_key)

    writer = ShortStoryWriter(org_key=args.org_key, api_key=args.api_key)
    story, total_cost, time = writer.author(prompt=args.prompt, n_chapters=args.n_chapters)
    formatter = StoryFormatter()

    formatter.write_to_file(story, args.output_dir, total_cost, time, args.filetype)

if __name__ == '__main__':
    main()