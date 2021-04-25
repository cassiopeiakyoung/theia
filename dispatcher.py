import video, image, audio
import discord, aiohttp, os, asyncio
import config

async def dispatch(msg: discord.Message):
    msgLower = msg.content.lower()
    
    if msg.attachments:
        for attachment in msg.attachments:
            for attachment in msg.attachments:
                header = header_type(attachment.url)
                print(f'[ATTACHMENT FOUND] type: {attachment.content_type}')
                if header == 'VIDEO': 
                    await video.process_file(await save_attachment(attachment, msg), msg)
                elif header == 'GIF':
                    await video.process_file(await save_attachment(attachment, msg), msg)
                elif header == 'PICTURE':
                    await image.process_file(await save_attachment(attachment, msg), msg)
                elif header == 'AUDIO':
                    await audio.process_file(await save_attachment(attachment, msg), msg)
                else:
                    print('failed to get file type from attachment')
        
    elif msg.embeds or (msgLower.__contains__('cdn.') or msgLower.__contains__('media.')):
        pass
'''         for embed in msg.embeds:
            if header_type(msgLower) is not None:
                    header = header_type(msgLower)
                    if header == 'VIDEO': 
                        print(await save_embed(embed, msg))
                        video.process_file(embed, True)
                    elif header == 'GIF':
                        print(await save_embed(embed, msg))
                        video.process_file(embed, False)
                    elif header == 'PICTURE':
                        print(await save_embed(embed, msg))
                        image.process_file(embed)
                    elif header == 'AUDIO':
                        print(await save_embed(embed, msg))
                        audio.process_file(embed)
                    else:
                        print('failed to get file type from attachment')
            else:
                await msg.reply('good embed')
                print(msgLower) '''
            

def header_type(msg: discord.Message):
    for key in config.FILE_HEADERS.keys():
        for header in config.FILE_HEADERS[key]:
            if msg.__contains__(header):
                return key
    return None

async def save_attachment(attachment, msg):
    if attachment.url and attachment.id:
        await attachment.save(f'temp/{msg.id}{attachment.filename}')
        return(f'temp/{msg.id}{attachment.filename}')
    else:
        print('[ATTACHMENT SAVING] attachment save requested did not have a .url or a .id')
        
async def save_embed(embed, msg):
    if embed.url:
        async with aiohttp.ClientSession() as session:
            async with session.get(embed.url) as resp:
                if resp.status == 200:
                    attachment_name = os.path.basename(embed.url)
                    with open(f'temp/{msg.id}', "wb") as file:
                        file.write(await resp.read())
    else:
        print('[EMBED SAVING] embed save requested did not have any content attached to it')