import asyncio

from settings import WEBHOOK_DISPATCHER, logger


if __name__ == "__main__":
    if WEBHOOK_DISPATCHER:
        from webhook_dispatcher import web, app
        from settings import WEB_SERVER_HOST, WEB_SERVER_PORT
        logger.info(f"Bot running on webhooks, HOST:{WEB_SERVER_HOST} PORT:{WEB_SERVER_PORT}")
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    else:
        from polling_dispatcher import main
        logger.info("Bot started working")
        asyncio.run(main())
        logger.info("Bot is off")
