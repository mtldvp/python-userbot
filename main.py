from pyrogram import Client, filters
# import logging
import uvloop
import httpx
import os
# from uvicorn import run as uvicorn_run
# import uvicorn
# from fastapi import FastAPI
import dotenv

dotenv.load_dotenv()

uvloop.install()


api_id = int(os.getenv("API_ID"))   
api_hash = os.getenv("API_HASH")  
coinapi_key = os.getenv("COINAPI_KEY")

# logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


app = Client("my_account", api_id=api_id, api_hash=api_hash)
# webapp = FastAPI()



ALLOWED_GROUPS = {-4235337165, -1001789106500}
#-1001789106500 croco
#testloggroup -4235337165

@app.on_message(filters.group & filters.command('crypto'))
async def echo(client, message):
    if message.chat.id not in ALLOWED_GROUPS:
        # logging.info(f"Received message from non-allowed group: {message.chat.id}")
        await app.send_message(chat_id=-4235337165, text=f"Received message from non-allowed group: {message.chat.id}")
        return

    try:
        if len(message.command) != 3 or not message.command[1].isalpha():
            await message.reply("Please provide a coin ticker and amount. Usage: `/crypto btc 1`")
            await app.send_message(chat_id=-4235337165, text=f"Wrong command usage - chat_id: {message.chat.id} - chat_message: {message.text}")
            # logging.warning(f"Wrong coin name provided - chat_id: {message.chat.id} - chat_message: {message.text}")
            return
        
        coin_ticker = message.command[1].upper().strip()
        # logging.info(f"Fetching data for coin: {coin_ticker}")
        await app.send_message(chat_id=-4235337165, text=f"Fetching data for coin: {coin_ticker}")

        url = f"https://api.binance.com/api/v3/ticker/price?symbol={coin_ticker}USDT" 

        headers = {
        'Accept': 'application/json',
        }

        try:
            coin_count = float(message.command[2].lower().strip())
        except:
            await message.reply("Please provide a coin ticker and amount. Usage: `/crypto btc 1`")
            await app.send_message(chat_id=-4235337165, text=f"Wrong command usage - chat_id: {message.chat.id} - chat_message: {message.text}")
            # logging.warning(f"Wrong coin name provided - chat_id: {message.chat.id} - chat_message: {message.text}")
            return
            
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)

            if response.status_code != 200:
                # logging.error(f"API Error: Status code {response.status_code} - Message: {response.text}")
                await app.send_message(chat_id=-4235337165, text=f"API Error: Status code {response.status_code} - Message: {response.text} - chat_id: {message.chat.id} - url: {url}")
                await app.send_message(
                    chat_id=message.chat.id,
                    text='Oops wrong ticker',
                    reply_to_message_id=message.id
                )
                return
            data = response.json()

            if 'error' in data:
                raise ValueError(f"Invalid ticker: {data['error']}")


        if not data:
            await message.reply("Coin not found.")
            # logging.warning(f"Coin not found: {coin_ticker}")
            await app.send_message(chat_id=-4235337165, text=f"Coin not found: {coin_ticker}")
            return
        
        rate = float(data['price'])

        if rate > 0.001:
            reply_message = f'''
        The current price of {coin_count} {coin_ticker} is **${rate*coin_count:.4f}** 
'''
        else:
            reply_message = f'''
        The current price of {coin_count} {coin_ticker} is **${rate*coin_count:.12f}** 
'''
        
        await app.send_message(
            chat_id=message.chat.id,
            text=reply_message,
            reply_to_message_id=message.id
        )
        # logging.info(f"Sent message: {reply_message} - to chat_id: {message.chat.id}")

        await app.send_message(chat_id=-4235337165, text=f"Sent message: {reply_message} - to chat_id: {message.chat.id}")






    except httpx.RequestError as e:
        # logging.error(f"An error occurred: {e}")
        await message.reply(f"Error fetching data: {e}")
        await app.send_message(chat_id=-4235337165, text=f"Error fetching data: {e}\nchat_id: {message.chat.id}")


# def run_webapp():
#     uvicorn_run(webapp, host='0.0.0.0', port=8000)

app.run()
print("BOT END")