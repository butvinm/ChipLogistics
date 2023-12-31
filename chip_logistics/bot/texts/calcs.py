"""Calculations texts."""


START = 'Расчет стоимости позиций'

BACK_TO_MENU = '🔙 Вернуться в меню'

ASK_CUSTOMER_NAME = 'Укажите имя клиента:'

ADD_ITEM_BTN = 'Добавить позицию'

ARTICLE_SELECT = 'Выберите позицию или введите наименование и пошлину в ручную'

ARTICLE_MANUAL_INPUT = 'Ввести данные в ручную'

ASK_NAME = 'Укажите наименование позиции:'

ASK_DUTY_FEE_RATIO = 'Укажите пошлину на позицию (например, "9.5" для наценки в 9.5%):'

BAD_DUTY_FEE_RATIO = 'Неверный формат. Пошлина должна быть числом, например, например, "9.5" для наценки в 9.5%. Попробуйте снова'

ASK_ITEM_NAME = 'Укажите наименование позиции:'

ASK_ITEM_COUNT = 'Укажите количество единиц позиции:'

BAD_ITEM_COUNT = 'Неверный формат. Количество должно быть числом. Попробуйте снова:'

ASK_ITEM_UNIT_WEIGHT = 'Укажите вес одной единицы в кг:'

BAD_ITEM_UNIT_WEIGHT = 'Неверный формат. Вес должно быть числом. Попробуйте снова:'

ASK_ITEM_PRICE_CURRENCY = 'Укажите валюту цены:'

ASK_ITEM_UNIT_PRICE = 'Укажите цену единицы в {currency}:'

BAD_ITEM_UNIT_PRICE = 'Неверный формат. Цена должна быть числом. Попробуйте снова:'

CONTINUATION_MENU = """Добавленные позиции:

{items_data}
"""

ITEM_DATA = """<b>Наименование:</b> {name}
Количество: {count}
Вес единицы: {unit_weight}
Цена за единицу: {unit_price} {price_currency}"""

STOP_BTN = 'Завершить'

CONTACT_SEARCH_MENU = 'Укажите контакт из AmoCRM, к которому будет прикреплен файл с расчетами.'

SEARCH_CONTACT_BTN = 'Найти контакт'

SKIP_CONTACT_BTN = 'Пропустить'

ASK_SEARCH_QUERY = 'Введите запрос для поиска контакта. Это может быть часть имени, телефона или других данных из AmoCRM:'

SEARCH_RESULT = 'Найденные контакты'

CONTACT_SELECTED = 'Контакт выбран'

CONTINUE_SEARCH_CONTACT_BTN = 'Искать еще'

CALCS_RESULT = 'Результаты расчетов'

FINISH_BTN = 'Завершить'
