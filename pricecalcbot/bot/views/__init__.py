"""Bot views.

Views are functions, responsible for sending messages, keyboards, files
and do other things, related to user interaction.

Views functions can be reused in many routers.

Views with name like `show_<something>` expect editable messages
(ones those sent by bot) an will update them text or keyboard.

Views with name like `send_<something>` will send new messages.
"""
