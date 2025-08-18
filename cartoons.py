import compuglobal.aio


async def get_gif(search_string: str, show: str = "simpsons"):
    if show.lower() == "simpsons":
        client = compuglobal.aio.Frinkiac()
    elif show.lower() == "futurama":
        client = compuglobal.aio.Morbotron()
    else:
        raise ValueError("Unsupported show. Use 'simpsons' or 'futurama'.")

    screencap = await client.search_for_screencap(search_string)
    gif = await screencap.get_gif_url()
    return gif
