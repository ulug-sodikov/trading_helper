# Trading Helper
Django App that help traders to track the price of trading instruments. It sends notifications to telegram if the price hits specified value.
## How to run?
1. Build docker image:
   ```
   bash build_image.sh
   ```
4. Run docker container:  
   ```
   docker compose -f docker-compose.yml up -d trading_helper_web_service
   ```
