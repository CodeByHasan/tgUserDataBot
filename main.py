import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError

# If you have a keep_alive script
from keep_alive import keep_alive

keep_alive()

# Initialize bot and dispatcher
bot = Bot('TOKEN')
dp = Dispatcher()

@dp.message(Command(commands=['start']))
async def start_command(message: types.Message):
    greeting = (
        "Hello! I'm `@tgUserDataBot`. I'm here to provide you with your public information.\n\n"
        "For your information, I can retrieve your profile photo, name, user ID, username, language, and premium subscriber status. "
        "To get your information, simply use the command /getinfo.\n\n"
        "Please subscribe to our eBook sharing channel: @FicShelf\n"
        "Join our discussion group: @FicTalk"
    )
    await message.reply(greeting, parse_mode='Markdown')
    
    # Send user information in the next message
    await send_user_info(message.from_user)

async def send_user_info(user: types.User):
    response = (
        f"**Name:** `{user.first_name} {user.last_name if user.last_name else ''}`\n"
        f"**User ID:** `{user.id}`\n"
        f"**Username:** @{user.username if user.username else 'N/A'}\n"
        f"**Language:** `{user.language_code if user.language_code else 'N/A'}`\n"
        f"**Premium Subscriber:** `{'Yes' if user.is_premium else 'No'}`\n"
    )
    
    # Retrieve user's profile photo
    profile_photos = await bot.get_user_profile_photos(user.id)
    
    if profile_photos.total_count > 0:
        # Get the file ID of the first profile photo
        file_id = profile_photos.photos[0][-1].file_id
        await bot.send_photo(user.id, photo=file_id, caption=response, parse_mode='Markdown')
    else:
        await bot.send_message(user.id, response, parse_mode='Markdown')

@dp.message(Command(commands=['getinfo']))
async def get_user_info(message: types.Message):
    # Send the current user's information
    await send_user_info(message.from_user)

async def main():
    # Start polling
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
