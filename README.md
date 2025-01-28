# Trading Helper
App that help traders to track the price of trading instruments. It sends notifications to telegram if the price hits specified value.
## How to run?
1. Create .env file in the root directory with the following content:
   ```
   SECRET_KEY=<DJANGO SECRET KEY>
   DEBUG=<DJANGO DEBUG MODE>        # Allowed values: True, False.
   ```
2. Move to `docker` directory:
   ```
   cd docker/
   ```
3. Build docker image:
   ```
   bash build_trading_helper_web_image.sh
   ```
4. Run docker container:  
   ```
   docker compose -f docker-compose.yml up -d trading_helper_web_service
   ```
