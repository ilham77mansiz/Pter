from userbot.events import register
from userbot import CMD_HELP, bot


@register(outgoing=True, pattern=r"^\.joinvc (?:(now)|(.*) - (.*))")
async def joinvc(msg: Message):
    """ join voice chat """
    global CHAT_NAME, CHAT_ID  # pylint: disable=global-statement

    await msg.delete()

    if CHAT_NAME:
        await reply_text(msg, f"`Already joined in {CHAT_NAME}`")
        return

    CHAT_ID = msg.chat.id
    CHAT_NAME = msg.chat.title
    try:
        await call.start(CHAT_ID)
    except RuntimeError:
        try:
            peer = await msg.client.resolve_peer(CHAT_ID)
            await msg.client.send(
                functions.phone.CreateGroupCall(
                    peer=peer, random_id=2
                )
            )
            await asyncio.sleep(3)
            await call.start(CHAT_ID)
        except Exception as err:
            await msg.err(str(err))
            CHAT_ID, CHAT_NAME = 0, ""


@register(outgoing=True, pattern=r"^\.leavevc (?:(now)|(.*) - (.*))")
@vc_chat
async def leavevc(msg: Message):
    """ leave voice chat """
    global CHAT_NAME, CHAT_ID  # pylint: disable=global-statement

    await msg.delete()

    if CHAT_NAME:
        await call.stop()
        await asyncio.sleep(2)
        CHAT_NAME = ""
        CHAT_ID = 0
    else:
        await reply_text(msg, "`I didn't find any Voice-Chat to leave")




@register(outgoing=True, pattern=r"^\.playvc (?:(now)|(.*) - (.*))")
@vc_chat
async def play_music(msg: Message):
    """ play music in voice chat """

    if not CHAT_ID or msg.chat.id != CHAT_ID:
        return

    if msg.input_str:
        if re.match(yt_regex, msg.input_str):
            QUEUE.append(msg)
            if PLAYING:
                text = SCHEDULED.format(
                    title="Song", link=msg.input_str, position=len(QUEUE))
                await reply_text(msg, text)
        else:
            mesg = await reply_text(msg, f"Searching `{msg.input_str}` on YouTube")
            title, link = await _get_song(msg.input_str)
            if link:
                await mesg.delete()
                mesg = await reply_text(msg, f"Found [{title}]({link})")
                QUEUE.append(mesg)
                if PLAYING:
                    text = SCHEDULED.format(
                        title=title, link=mesg.link, position=len(QUEUE))
                    await reply_text(msg, text)
            else:
                await mesg.edit("No results found.")
    elif msg.reply_to_message and msg.reply_to_message.audio:
        QUEUE.append(msg)
        replied = msg.reply_to_message
        if PLAYING:
            text = SCHEDULED.format(
                title=replied.audio.title, link=replied.link, position=len(QUEUE))
            await reply_text(msg, text)
    else:
        return await reply_text(msg, "Input not found")

    if not PLAYING:
        await handle_queue()


@register(outgoing=True, pattern=r"^\.queue (?:(now)|(.*) - (.*))")
@vc_chat
async def view_queue(msg: Message):
    """ View Queue """

    await msg.delete()

    if not QUEUE:
        out = "`Queue is empty`"
    else:
        out = f"**{len(QUEUE)} Songs in Queue:**\n"
        for i in QUEUE:
            replied = i.reply_to_message
            if replied and replied.audio:
                out += f"\n - [{replied.audio.title}]"
                out += f"({replied.link})"
            else:
                link = i.input_str
                if "Found" in i.text:
                    link = i.entities[0].url
                out += f"\n{link}"

    await reply_text(msg, out)


@register(outgoing=True, pattern=r"^\.skipsong (?:(now)|(.*) - (.*))")
@vc_chat
async def skip_music(msg: Message):
    """ skip music in vc """

    await msg.delete()

    await _skip()
    await reply_text(msg, "`Skipped`")


@register(outgoing=True, pattern=r"^\.pause (?:(now)|(.*) - (.*))")
@vc_chat
async def pause_music(msg: Message):
    """ paise music in vc """

    await msg.delete()

    call.pause_playout()
    await reply_text(msg, "⏸️ **Paused** Music Successfully")



@register(outgoing=True, pattern=r"^\.resume (?:(now)|(.*) - (.*))")
@vc_chat
async def resume_music(msg: Message):
    """ resume music in vc """

    await msg.delete()

    call.resume_playout()
    await reply_text(msg, "◀️ **Resumed** Music Successfully")

@register(outgoing=True, pattern=r"^\.stopmusic (?:(now)|(.*) - (.*))")
@vc_chat
async def stop_music(msg: Message):
    """ stop music in vc """

    await msg.delete()
    await _skip(True)

    await reply_text(msg, "`Stopped Userge-Music.`")

CMD_HELP.update(
    {
        "vc": ".vc\
    \nBroadcast ke Seluruh Grup."
    })
