import re

from telethon.tl.functions.users import GetFullUserRequest
from userbot.events import register


@register(outgoing=True, pattern="^.addsudo ?(.*)")
async def _(event):
    if Var.BOT_MODE:
        try:
            if event.sender_id != Var.OWNER_ID:
                return await eod(event, "`Sudo users can't add new sudos!`", time=10)
        except BaseException:
            pass
    else:
        if event.sender_id != ultroid_bot.uid:
            return await eod(event, "`Sudo users can't add new sudos!`", time=10)
    ok = await eor(ult, "`Updating SUDO Users List ...`")
    if event.reply_to_msg_id:
        replied_to = await event.get_reply_message()
        id = replied_to.sender.id
        user = await event.client(GetFullUserRequest(int(id)))
        sed.append(id)
        if id == ultroid_bot.me.id:
            return await ok.edit("You cant add yourself as Sudo User...")
        elif is_sudo(id):
            return await ok.edit(
                f"[{user.user.first_name}](tg://user?id={id}) `is already a SUDO User ...`",
            )
        elif add_sudo(id):
            udB.set("SUDO", "True")
            return await ok.edit(
                f"**Added [{user.user.first_name}](tg://user?id={id}) as SUDO User**",
            )
        else:
            return await ok.edit("`SEEMS LIKE THIS FUNCTION CHOOSE TO BREAK ITSELF`")

    args = ult.pattern_match.group(1).strip()

    if re.search(r"[\s]", args) is not None:
        args = args.split(" ")
        msg = ""
        sudos = get_sudos()
        for item in args:
            user = ""
            try:
                user = await ult.client(GetFullUserRequest(int(item)))
            except BaseException:
                pass
            if not hasattr(user, "user"):
                msg += f"• `{item}` __Invalid UserID__\n"
            elif item in sudos:
                msg += f"• [{user.user.first_name}](tg://user?id={item}) __Already a SUDO__\n"
            elif add_sudo(item.strip()):
                msg += (
                    f"• [{user.user.first_name}](tg://user?id={item}) __Added SUDO__\n"
                )
            else:
                msg += f"• `{item}` __Failed to Add SUDO__\n"
        return await ok.edit(f"**Adding Sudo Users :**\n{msg}")

    id = args.strip()
    user = ""

    try:
        user = await event.client(GetFullUserRequest(int(i)))
    except BaseException:
        pass

    if not id.isdigit():
        return await ok.edit("`Integer(s) Expected`")
    elif not hasattr(user, "user"):
        return await ok.edit("`Invalid UserID`")
    elif is_sudo(id):
        return await ok.edit(
            f"[{user.user.first_name}](tg://user?id={id}) `is already a SUDO User ...`",
        )
    elif add_sudo(id):
        udB.set("SUDO", "True")
        return await ok.edit(
            f"**Added [{user.user.first_name}](tg://user?id={id}) as SUDO User**\n\nDo Restart",
        )
    else:
        return await ok.edit(f"**Failed to add `{id}` as SUDO User ... **")
