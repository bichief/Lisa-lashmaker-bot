import re


async def validator(phone):
    valid_phone = [int(nomber) for nomber in phone if nomber.isdigit()]
    try:
        if valid_phone[0] == 7:
            phone = '+{}{}{}{}{}{}{}{}{}{}{}'.format(*valid_phone)
            return phone
        return None
    except:
        return None
