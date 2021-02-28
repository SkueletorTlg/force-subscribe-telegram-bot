import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="❗ Únase al 'canal' mencionado y presione el botón 'Desactivar mute' nuevamente.", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="❗ Los administradores te silenciaron por otras razones.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention} Estoy tratando de remover el mute, pero no puedo hacerlo porque no soy un administrador en este chat, agrégueme como administrador nuevamente.**\n__Me voy de este chat :(...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❗ Advertencia: No haga clic en el botón si no estás muteado.", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              "Hola {}, todavía no estás **suscrito** a mi [canal](https://t.me/{}). [Únase](https://t.me/{}) y **presione el botón de abajo** para que puedas hablar.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("Desactivar mute", callback_data="onUnMuteRequest")]]
              )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **No soy un administrador aquí.**\n__Hazme administrador con permiso de usuario de baneo y agrégame de nuevo.\n#Me voy de este chat :(...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **No soy administrador en @{channel}**\n__Hazme administrador en el canal y agrégame de nuevo.\nMe voy de este chat :(...__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Forzar suscripción se deshabilitó correctamente.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**Desactivando el mute todos los miembros silenciados por mí...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **He quitado el mute a todos los miembros que había silenciado anteriormente.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **No soy administrador en este chat.**\n__No puedo remover el mute a los miembros porque no soy un administrador en este chat, hazme administrador con permiso de usuario de baneo.__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          message.reply_text(f"✅ **Forzar suscripción está habilitado**\n__Forzar suscripción está habilitado, todos los miembros del grupo deben suscribirse a este [canal](https://t.me/{input_str}) para enviar mensajes en este grupo.__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **No soy un administrador en el canal**\n__No soy administrador en el [canal](https://t.me/{input_str}). Agrégame como administrador para habilitar ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Nombre de usuario de canal no válido.**")
        except Exception as err:
          message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **Forzar suscripción está habilitado en este chat.**\n__Para este [Canal](https://t.me/{sql.fs_settings(chat_id).channel})__", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Forzar suscripción está deshabilitado en este chat.**")
  else:
      message.reply_text("❗ **Se requiere creador de grupo**\n__Tienes que ser el creador del grupo para hacer eso.__")
