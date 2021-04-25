import discord, os, asyncio
import config

async def scan_for_blacklisted_words(msg: discord.Message, possible_words_in_attachment, SentFrom):
    for banned_phrase in config.BLACKLISTED:
        if possible_words_in_attachment.lower().__contains__(banned_phrase):
            await msg.delete()
            print(f'deleted banned phase {banned_phrase}')
            os.remove(SentFrom)