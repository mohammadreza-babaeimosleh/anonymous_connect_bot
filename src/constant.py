from types import SimpleNamespace

from src.utils.keyboard import create_keyboard

# different keys that can be used in keyboards
keys = SimpleNamespace(
    random_connect=":technologist: Random Connect",
    setting=":gear: Setting",
    send_message=":envelope: Send Messagee",
    exit=":cross_mark: Exit",
)

# savaed keyboards to use
keyboards = SimpleNamespace(
    main=create_keyboard(keys.random_connect, keys.setting, keys.send_message),
    exit=create_keyboard(keys.exit),
)

# different states that a user can has
states = SimpleNamespace(
    main="Main Menu", random_connect="Random Connect", connected="Connected"
)

