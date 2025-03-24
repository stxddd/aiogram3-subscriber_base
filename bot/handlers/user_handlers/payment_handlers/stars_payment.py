import json
from datetime import datetime

from aiogram import Bot, Router, F
from aiogram.exceptions import TelegramAPIError
from aiogram.filters import Command
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.methods.refund_star_payment import RefundStarPayment

from bot.decorators.admin_required import admin_required
from bot.handlers.admin_handlers.notification_handlers.marzban.accept_create_connection import handle_accept_marzban_client
from bot.handlers.admin_handlers.notification_handlers.marzban.accept_extend_connection import handle_reject_marzban_client
from bot.templates.admin_templates.messages_templates import refunded_succsses_message
from bot.templates.user_templates.errors_templates import payment_create_error
from bot.templates.user_templates.message_templates import (
    payment_title,
    extend_payment_description,
    accept_payment_description,
)
from bot.templates.admin_templates.errors_templates import refunded_error, payment_error

router = Router()


async def process_activate_subscription_pay_command(message: Message, price: int, payload, os_name, date_to) -> None:
    try:
        payload = json.dumps(payload)
        prices = [LabeledPrice(label='Stars Payment', amount=price)]
        await message.answer_invoice(
            title=payment_title(date_to=date_to, os_name=os_name),
            description=accept_payment_description,
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter='activate-subscription',
            payload=payload,
        )
    except TelegramAPIError:
        await message.answer(payment_create_error)
        
async def process_extend_subscription_pay_command(message: Message, price: int, payload, os_name, date_to) -> None:
    try:
        payload = json.dumps(payload)
        prices = [LabeledPrice(label='Stars Payment', amount=price)]
        await message.answer_invoice(
            title=payment_title(date_to=date_to, os_name=os_name),
            description=extend_payment_description,
            provider_token="",
            currency="XTR",
            prices=prices,
            start_parameter='extend-subscription',
            payload=payload,
        )
    except TelegramAPIError:
        await message.answer(payment_create_error)


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(ok=True)

    
@router.message(F.successful_payment)
async def process_successful_payment(message: Message) -> None:
    payload = json.loads(message.successful_payment.invoice_payload)

    print(message.successful_payment.telegram_payment_charge_id)
    
    if payload["type"] == 'activate-subscription-payload':
        await handle_accept_marzban_client(message=message,
                                           connection_id = payload["connection_id"])
    elif payload["type"] == 'extend-subscription-payload':
        await handle_reject_marzban_client(message=message,
                                           connection_id = payload["connection_id"], 
                                           price = payload["new_price"],
                                           date_to = datetime.strptime(payload["new_date_to"], "%Y-%m-%d %H:%M:%S"))

    else:
        await message.answer(payment_error)
    
    
    
@router.message(Command("refund"))
@admin_required
async def process_refund(message: Message, bot: Bot) -> None:
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer(refunded_error)
        await message.delete()
        return

    transaction_id = parts[1]
    try:
        result = await bot(RefundStarPayment(
            user_id=message.from_user.id,
            telegram_payment_charge_id=transaction_id
        ))

        await message.answer(
            refunded_succsses_message(transaction_id) if result else refunded_error
        )
        await message.delete()
    except TelegramAPIError:
        await message.answer(refunded_error)
        await message.delete()