import os

class Config():
  ENV = bool(os.environ.get('ENV', False))
  if ENV:
    BOT_TOKEN = os.environ.get("1622814733:AAEyxcB5n6FwzBVIT2LgO-oyH2iqWwOgO2M", None)
    DATABASE_URL = os.environ.get("DATABASE_URL", None)
    APP_ID = os.environ.get("2788465", 6)
    API_HASH = os.environ.get("fc41e33d78927150ad3f81c257f7cf31", None)
    SUDO_USERS = list(set(int(x) for x in os.environ.get("1192065197").split()))
    SUDO_USERS.append(1192065197)
    SUDO_USERS = list(set(SUDO_USERS))
  else:
    BOT_TOKEN = "1622814733:AAEyxcB5n6FwzBVIT2LgO-oyH2iqWwOgO2M"
    DATABASE_URL = ""
    APP_ID = "2788465"
    API_HASH = "fc41e33d78927150ad3f81c257f7cf31"
    SUDO_USERS = list(set(int(x) for x in ''.split()))
    SUDO_USERS.append(1192065197)
    SUDO_USERS = list(set(SUDO_USERS))


class Messages():
      HELP_MSG = [
        ".",

        "**Force Subscribe**\n__Puedo obligar a los miembros del grupo a unirse a un canal específico antes de enviar mensajes en el grupo.\nSilenciaré a los miembros si no se han unido a tu canal, les diré que se unan al canal y que se desactiven el mute ellos mismos presionando un botón.__",
        
        "**Configuración**\n__En primer lugar, agrégueme al grupo como administrador con permiso de baneo de usuarios y en el canal como administrador. \nNota: solo el creador del grupo puede configurarme y abandonaré el chat si no soy un administrador en el chat.__",
        
        "**Comandos**\n__/ForceSubscribe - Para obtener la configuración actual.\n/ForceSubscribe no/off/disable - Para desactivar ForceSubscribe.\n/ForceSubscribe {channel username} - Para encender y configurar el canal.\n/ForceSubscribe clear - Para quitar el mute a todos los miembros que fueron silenciados por mí.__",
        
        "**Creado por @DKzippO**"
      ]

      START_MSG = "**Hola [{}](tg://user?id={})**\n__Puedo obligar a los miembros a unirse a un canal específico antes de escribir mensajes en el grupo.\nObtenga más información en /help__"
