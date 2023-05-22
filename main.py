import asyncio
import os
import sys

import openai
from dotenv import load_dotenv

from cli.commands import process_commands


async def main():
    # Load .env settings into environment
    load_dotenv()
    openai.api_key = os.getenv('OPENAI_API_KEY')

    if os.getenv('OPENAI_API_KEY') == None:
        print("OPENAI_API_KEY not set in environment. See README.md for info.")
        sys.exit()

    args = sys.argv[1:]
    if not args:
        print("No commands provided, see -help for info")
        return

    await process_commands(args)

if __name__ == '__main__':
    asyncio.run(main())