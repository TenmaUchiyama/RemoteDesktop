# monitor_manager.py
class MonitorManager:
    monitor_data = {}

    @classmethod
    def add_monitor(cls, monitor_id, monitor_type, monitor):
        cls.monitor_data[monitor_id] = {"monitor_type": monitor_type, "monitor": monitor }
        

    @classmethod
    def get_monitors(cls, monitor_id):
        return cls.monitor_data.get(monitor_id)