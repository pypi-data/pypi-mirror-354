from .application import Application


def run():
    from rich.traceback import install

    install(show_locals=False, word_wrap=True, suppress=["rich"])

    with Application() as app:
        app.run()
