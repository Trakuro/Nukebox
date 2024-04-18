from nonebot import on_command

whoami = on_command("whoami")


@whoami.handle()
async def handle_function():
    await whoami.finish("Evanktis.")
