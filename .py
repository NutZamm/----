import os
import random
import requests
import json

from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Define constants
STOCKS = {
    "AAPL": "Apple Inc.",
    "GOOG": "Alphabet Inc.",
    "TSLA": "Tesla Inc."
}

MAX_QUANTITY = 1000
MAX_PRICE_CHANGE_PERCENTAGE = 5
MIN_INVESTMENT = 1000

# Define global variables
user_history = {}

# Define helper functions
def calculate_possible_outcomes(trade_history, current_price, investment):
    possible_outcomes = {}
    for trade in trade_history:
        if trade["action"] == "BUY":
            sell_price = current_price + current_price * random.uniform(0, MAX_PRICE_CHANGE_PERCENTAGE) / 100
            quantity = min(trade["quantity"], MAX_QUANTITY)
            profit = quantity * (sell_price - trade["price"])
            possible_outcomes[trade["id"]] = profit
    return possible_outcomes

def save_trade_history(user_id, stock_name, action, price, quantity):
    trade_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
    trade = {
        "id": trade_id,
        "stock": stock_name,
        "action": action,
        "price": price,
        "quantity": quantity
    }
    trade_history = user_history.get(user_id, [])
    trade_history.append(trade)
    user_history[user_id] = trade_history

def send_alert(user_id, stock_name, current_price, investment):
    trade_history = user_history.get(user_id, [])
    possible_outcomes = calculate_possible_outcomes(trade_history, current_price, investment)
    max_profit = max(possible_outcomes.values())
    if max_profit < 0:
        loss_percent = abs(max_profit) / investment * 100
        if loss_percent > 10:
            message = f"WARNING: You have a potential loss of {loss_percent:.2f}% in {stock_name} ({current_price}). Consider selling."
            webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
            payload = {
                "content": message
            }
            headers = {
                "Content-Type": "application/json"
            }
            requests.post(webhook_url, json=payload, headers=headers)

# Define Discord client
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

# Define bot commands
@client.command()
async def stocks(ctx):
    message = "Available stocks:\n"
    for symbol, name in STOCKS.items():
        message += f"{symbol} - {name}\n"
    await ctx.send(message)

@client.command()
async def buy(ctx, stock_name, price, quantity):
    user_id = str(ctx.author.id)
    investment = int(price) * int(quantity)
    if investment < MIN_INVESTMENT:
        await ctx.send(f"Minimum investment is {MIN_INVESTMENT}.")
        return
    if stock_name not in STOCKS:
        await ctx.send(f"Invalid stock name.")
        return
    current_price = int(price) + int(price) * random.uniform(-MAX_PRICE_CHANGE_PERCENTAGE, MAX_PRICE_CHANGE_PERCENTAGE) / 100
