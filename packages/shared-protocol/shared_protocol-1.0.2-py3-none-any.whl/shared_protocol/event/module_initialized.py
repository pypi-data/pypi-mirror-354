from shared_protocol.event.base_event import BaseEvent


class ModuleInitialized(BaseEvent):
    modules_data: list = []
    ip_data: dict
