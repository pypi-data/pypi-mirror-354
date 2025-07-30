import logging
from ..message import AgentLogEvent

from ..conf import TimeplusAgentConfig

log_stream_name = "agent_log"


class TimeplusHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        config = TimeplusAgentConfig()
        self.client = config.get_timeplusd_client()
        self.db = config.get_aiservice_db()
        self._create_log_stream()

    def _create_log_stream(self):
        self.client.execute(
            f"""CREATE STREAM IF NOT EXISTS {self.db}.{log_stream_name} (
            agent string,
            sender string,
            receiver string,
            system_message string,
            user_prompt string,
            response string,
            model string,
            timestamp datetime64(3)
        )"""
        )

    def _insert_log_event(self, log_event: AgentLogEvent):
        try:
            self.client.execute(
                f"INSERT INTO {self.db}.{log_stream_name} (agent,sender,receiver,system_message,user_prompt,response,model,timestamp) VALUES",
                [
                    [
                        log_event.agent_description,
                        log_event.sender_topic,
                        log_event.receiver_topic,
                        log_event.system_message,
                        log_event.user_prompt,
                        log_event.response,
                        log_event.model,
                        log_event.timestamp,
                    ]
                ],
            )
        except Exception as e:
            print(e)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            if isinstance(record.msg, AgentLogEvent):
                self._insert_log_event(record.msg)
        except Exception:
            self.handleError(record)
