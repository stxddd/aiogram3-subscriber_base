from bot.utils.data_processing.date_converter import format_date
from bot.config import settings
from bot.templates.user_templates.keyboards_templates import my_connections_text, renew_subscribtion_text

welcome_message = "Привет 🤖\n\n✅ Выбери, что хочешь сделать."
enter_os_message = "Выбери свою операционную систему."
enter_server_message = "Выбери желаемый для подключения регион."
def wait_for_payment_message(connection, key: int): return f"✅ Подключение \n\n{connection.os_name} | {format_date(connection.date_to)} | {connection.price} \n\nСсылка на оплату:\n{settings.PAYMENT_LINK} \n\n❗️Сумма: {connection.price}\n❗️В комментарии укажите: {key}\n\n"
def wait_for_extend_payment_message(connection, price, new_date_to, key: int): return f"✅ Оплатите продление \n\n{connection.os_name} | {format_date(connection.date_to)} | {connection.price} \nДо {format_date(new_date_to)}\n\nСсылка на оплату:\n{settings.PAYMENT_LINK} \n\n❗️Сумма: {price}\n❗️В комментарии укажите: {key}\n\n"
wait_for_admin_message = "✅ Дождитесь, когда администратор одобрит заявку."
rejected_message = "❌ Вам отказано в доступе"
get_instruction_os_message = '✅ Какое устройство Вы хотите подключть?'
marzban_day_limit_message = "❌ Слишком много запросов сегодня. Попробуйте завтра."
def buy_stars_tutorial(price): return f'Купить звезды выгоднее всего можно через @PremiumBot \n\n1) Отправьте ему команду /stars \n2) Выберите {price} звезд\n3) Оплатите звезды удобным способом\n4) Оплатите подключение'
android_instruction_message = "\n".join(('⚙️ Инструкция для подключения Android устройства\n\n',
                               '1. Установите приложение Hiddify. (https://play.google.com/store/apps/details?id=app.hiddify.com)\n',
                               '2. Скопируйте ключ доступа, отправленный сообщением ниже.\n',
                               '3. Запустите Hiddify. Сверху нажмите на "+" -> Добавить из буфера обмена.\n',
                               '4. Подключитесь, нажав на круглую кнопку на главном экране.\n\n',
                               f'✅ Приятного использования. По вопросам @{settings.ADMIN_USERNAME}'))
windows_instruction_message = "\n".join(('⚙️ Инструкция для подключения Windows устройства\n\n',
                               '1. Установите приложение Hiddify. (https://hiddify.com/)\n',
                               '2. Скопируйте ключ доступа, отправленный сообщением ниже.\n',
                               '3. Запустите Hiddify. Сверху нажмите на "+" -> Добавить из буфера обмена.\n',
                               '4. Подключитесь, нажав на круглую кнопку на главном экране.\n',
                               '5. ЕСЛИ вы не наблюдаете работы VPN, настройте систему:\n',
                               '5.1 Поставьте Регион "Другой" и переключите режим Системный прокси -> VPN в Настройках конфигурации.\n ',
                               '5.2 Необходимо установить запуск приложения от имени администратора в свойствах ярлыка.\n',
                               '5.3 После данного действия, перезапускаем приложение и включаем режим VPN в настройках слева от "+".\n\n',
                               f'✅ Приятного использования. По вопросам @{settings.ADMIN_USERNAME}'))
ios_instruction_message = "\n".join(('⚙️ Инструкция для подключения IOS устройства\n\n',
                               '1. Установите приложение v2RayTun из App Store.\n\n'
                               '2. Скопируйте ключ доступа, отправленный сообщением ниже.\n',
                               '3. Запустите v2RayTun. Сверху нажмите на "+" -> Добавить из буфера.\n',
                               '4. Подключитесь, нажав на круглую кнопку экране.\n\n',
                               f'✅ Приятного использования. По вопросам @{settings.ADMIN_USERNAME}'))
mac_instruction_message = "\n".join(('⚙️ Инструкция для подключения MacOS устройства\n\n',
                               '1. Установите приложение v2RayTun из App Store.\n\n'
                               '2. Скопируйте ключ доступа, отправленный сообщением ниже.\n',
                               '3. Запустите v2RayTun. Сверху нажмите на "+" -> Добавить из буфера.\n',
                               '4. Подключитесь, нажав на круглую кнопку экране.\n\n',
                               f'✅ Приятного использования. По вопросам @{settings.ADMIN_USERNAME}'))
androidTV_instruction_message = "\n".join((f'⚙️ Инструкция для подключения Android TV устройства\n\n',
                               f'1. Установите приложение Hiddify из Google Play\n',
                               f'2. Скачайте приложение Google TV. Откройте Google Play Store на своем Android-смартфоне или App Store на iPhone. В строке поиска введите «Google TV» и найдите официальное приложение от Google. Нажмите кнопку «Установить», чтобы загрузить и установить приложение на ваше устройство.\n',
                               f'2.1 Подключите телевизор к интернету. Запустите приложение Google TV на своем смартфоне. Войдите в приложение, используя свою учетную запись Google. Убедитесь, что вы используете ту же учетную запись, которую вы хотите подключить к телевизору. \n',
                               f'2.2 В приложении Google TV выберите опцию «Подключить к телевизору» или найдите кнопку «Добавить устройство» (может отображаться в виде значка телевизора). Приложение начнет искать доступные устройства. Убедитесь, что ваш телевизор включен и находится в одной сети Wi-Fi с вашим смартфоном. Когда ваш телевизор появится в списке доступных устройств, выберите его. \n',
                               f'3. Запустите Hiddify. Сверху нажмите на "+" -> Ввести вручную. С помощью режима клавиатуры в Google TV вставьте ключ из буфера в появившееся поле. Нажмите «Сохранить».\n',
                               f'4. Подключитесь, нажав на круглую кнопку на главном экране.\n\n',
                               f'✅ Приятного использования. По вопросам @{settings.ADMIN_USERNAME}'))
incorrect_os_message = '❌ Нет данных о такой ОС.'
enter_period_message = '⚙️ Выберите период подписки.'
def you_are_successfully_connected_message(date_to): return f'✅ Вы успешно подключены до {format_date(date_to)}'
def you_need_to_pay_message(connection): return f'⚠ Скоро истекает срок действия вашего подключения\n\n{connection.os_name} | {connection.price} | {format_date(connection.date_to)}\n\nЧтобы продлить:\n\n{my_connections_text} ->\n{connection.os_name} | {format_date(connection.date_to)} | {connection.price} ->\n{renew_subscribtion_text}'
def payment_title(os_name, date_to, server_name): return f'{server_name} {os_name} до {format_date(date_to)}.'
extend_payment_description = 'Оплатите продление'
accept_payment_description = "Оплатите создание"

