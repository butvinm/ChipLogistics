"""Filter for text messages.

Check that message text is not None and pass as router parameter.
"""


from aiogram import F

TextMessage = F.text.as_('text')
