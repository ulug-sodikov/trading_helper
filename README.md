# Trading Helper
App that help traders to track the price of trading instruments. It sends notifications to telegram if the price hits specified value.
## How to run the whole project?
1. Create .env file in the project's root directory.
2. Run metatrader5 api service.
   - Add the following variables to .env file:
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
     manually install metatrader via the opened window (other
     installations offered by the system can be denied).
      ```
      ![Screenshot from 2025-02-12 08-03-18.png](..%2F..%2FPictures%2FScreenshots%2FScreenshot%20from%202025-02-12%2008-03-18.png)
      ```
   - Wain until server is up (it happens silently in the background).
     To check if server is up, send HTTP GET request to 
     `http://localhost:8080/symbols_buffer`.
3. Run trading helper web service.
   - Add the following content to your `/etc/hosts` file:
      ```
      127.0.0.77 www.tradinghelper.com
      ```
   - Create a telegram bot by sending `/newbot` to `@BotFather`.
   - Send the `/setdomain` command to `@Botfather` to link 
     `www.tradinghelper.com` domain name to newly created bot.
   - Add the following variables to .env file:
      ```
      SECRET_KEY=<DJANGO_SECRET_KEY>
      DEBUG=<DJANGO_DEBUG_MODE>        # Allowed values: True, False.
   
      TG_BOT_USERNAME=<USERNAME_OF_YOUR_TG_BOT>
      TG_BOT_TOKEN=<TG_BOT_TOKEN>
      ```
   - Move to `docker` directory.
      ```
      cd docker/
      ```
   - Build docker image of trading helper web service.
      ```
      bash build_trading_helper_web_image.sh
      ```
   - Run docker container:  
      ```
      docker compose -f docker-compose.yml up -d trading_helper_web_service
      ```
