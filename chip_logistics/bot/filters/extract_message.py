"""Filter for message extracting from non-message events.

That filter get `message` attribute of event and pass to route parameters.
Commonly used with callbacks queries.
"""

from aiogram import F

ExtractMessage = F.message.as_('message')
