from nonebot.plugin import on_command
import random

dice = on_command("r", aliases={"roll"})


@dice.handle()
async def handle_function():
    result = random.randint(1, 20)
    await dice.finish(f"{result}")
