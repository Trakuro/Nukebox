from nonebot.plugin import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from .lib import Expression, roll_dice

roll = on_command("r", priority=10, block=True)


@roll.handle()
async def _(args: Message = CommandArg()):
    s = args.extract_plain_text()
    if s:
        result = Expression.from_str(s).eval()
        await roll.finish(str(result))
    else:
        result = roll_dice(1, 20)
        await roll.finish(str(result))
