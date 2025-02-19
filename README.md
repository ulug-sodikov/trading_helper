# Trading Helper 📈
App that help traders to track the price of trading instruments. It sends notifications to telegram if the price hits specified value.
## How to run the whole project?
1. Create `.env` file in the project's root directory.
2. Run `metatrader5_api_service`.
   - Add the following variables to `.env` file:
      ```
      MT5_LOGIN=<MT5_LOGIN>
      MT5_PASSWORD=<MT5_PASSWORD>
      MT5_SERVER=<MT5_SERVER>
      ```
   - Move to `docker` directory.
      ```
      cd docker/
      ```
   - Build docker image of metatrader5 api.
      ```
      bash build_metatrader5_api_image.sh
      ```
   - Run docker container.
      ```
      docker compose -f docker-compose.yml up -d metatrader5_api_service
      ```
   - In your browser open `http://localhost:3000`.
   - Wait until metatrader installation window is opened, then
     manually install metatrader5 via the opened window (installations 
     offered by the system can be denied).
   - Wain until server is up (it happens silently in the background).
     To check if server is up, send HTTP GET request to 
     `http://localhost:8080/symbols_buffer`.

3. Run `tg_bot_notifications_api_service`.
   - Create a telegram bot by sending `/newbot` to `@BotFather`.
   - Add the following variables to `.env` file in accordance to 
     your newly created telegram bot:
      ```
      TG_BOT_USERNAME=<USERNAME_OF_YOUR_TG_BOT>   # e.g. 'my_favorife_bot'
      TG_BOT_TOKEN=<TOKEN_OF_YOUR_TG_BOT>
      ```
   - Move to `docker` directory.
      ```
      cd docker/
      ```
   - Build docker image of tg bot notifications api service.
      ```
      bash build_tg_bot_notifications_api_image.sh
      ```
   - Run docker container:  
      ```
      docker compose -f docker-compose.yml up -d tg_bot_notifications_api_service
      ```

4. Run `trading_helper_web_service`.
   - Add the following content to your `/etc/hosts` file:
      ```
      127.0.0.77 www.tradinghelper.com
      ```
   - Send the `/setdomain` command to `@Botfather` to link 
     `www.tradinghelper.com` domain name to your telegram bot (from step 3).
   - Add the following variables to `.env` file:
      ```
      SECRET_KEY=<DJANGO_SECRET_KEY>
      DEBUG=<DJANGO_DEBUG_MODE>        # Allowed values: True, False.
      ```
   - Move to `docker` directory.
      ```
      cd docker/
      ```
   - Build docker image of trading helper web service.
      ```
      bash build_trading_helper_web_image.sh
      ```
   - Migrate (Create tables in database).
   - Run docker container:  
      ```
      docker compose -f docker-compose.yml up -d trading_helper_web_service
      ``` 

## Future improvements:
- Reconsider running price polling loop script in the `AppConfig.ready()` 
  (in `trading_helper_web_sevice`) since it accesses database during 
  initialization.
- Refresh the page automatically (in `trading_helper_web_sevice`'s frontend), 
  when real-time tick price hits target price.
