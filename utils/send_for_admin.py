from loader import bot

array = [1955750981, 417436565]


async def new_customer(name, phone):
    try:
        for row in array:
            await bot.send_message(chat_id=row,
                                   text=f'К вам записалась {name}\n'
                                        f'Контактный номер - {phone}\n\n'
                                        f'Созвонитесь, дабы узнать подробности :)')
    except:
        pass
