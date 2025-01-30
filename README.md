# Trading Helper
App that help traders to track the price of trading instruments. It sends notifications to telegram if the price hits specified value.
## How to run?
1. Add the following content to your `/etc/hosts` file:
   ```
   127.0.0.77 www.tradinghelper.com
   ```
2. Create a telegram bot by sending `/newbot` to `@BotFather`.
3. Send the `/setdomain` command to `@Botfather` to link `www.tradinghelper.com` domain to newly created bot.
4. Create .env file in the root directory with the following content:
   ```
   SECRET_KEY=<DJANGO_SECRET_KEY>
   DEBUG=<DJANGO_DEBUG_MODE>        # Allowed values: True, False.
   
   TG_BOT_USERNAME=<USERNAME_OF_YOUR_TG_BOT>
   TG_BOT_TOKEN=<TG_BOT_TOKEN>
   ```
5. Move to `docker` directory:
   ```
   cd docker/
   ```
6. Build docker image:
   ```
   bash build_trading_helper_web_image.sh
   ```
7. Run docker container:  
   ```
   docker compose -f docker-compose.yml up -d trading_helper_web_service
   ```
