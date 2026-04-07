from __future__ import annotations

from linearity_core.mav_params import fetch_parameter, set_parameter


class _FakeMessage:
    def __init__(self, param_id: str | bytes, param_value: float) -> None:
        self.param_id = param_id
        self.param_value = param_value


class _FakeMav:
    def param_request_read_send(self, *args, **kwargs) -> None:
        return None

    def param_set_send(self, *args, **kwargs) -> None:
        return None


class _FakeMaster:
    def __init__(self, messages: _FakeMessage | list[_FakeMessage]) -> None:
        self.mav = _FakeMav()
        self.target_system = 1
        self.target_component = 1
        if isinstance(messages, list):
            self._messages = list(messages)
        else:
            self._messages = [messages]

    def recv_match(self, *args, **kwargs):
        if not self._messages:
            return None
        return self._messages.pop(0)


def test_fetch_parameter_accepts_str_and_bytes_param_id() -> None:
    for param_id in ("MC_ROLLRATE_P", b"MC_ROLLRATE_P"):
        master = _FakeMaster(_FakeMessage(param_id, 0.15))
        assert fetch_parameter(master, "MC_ROLLRATE_P", timeout_s=0.01) == 0.15


def test_set_parameter_accepts_str_and_bytes_param_id() -> None:
    for param_id in ("MC_ROLLRATE_P", b"MC_ROLLRATE_P"):
        master = _FakeMaster(_FakeMessage(param_id, 0.18))
        assert set_parameter(master, "MC_ROLLRATE_P", 0.18, timeout_s=0.01) is True


def test_fetch_parameter_skips_empty_param_value() -> None:
    master = _FakeMaster(
        [
            _FakeMessage("MC_ROLLRATE_P", None),
            _FakeMessage("MC_ROLLRATE_P", 0.15),
        ]
    )
    assert fetch_parameter(master, "MC_ROLLRATE_P", timeout_s=0.01) == 0.15


def test_set_parameter_skips_empty_param_value() -> None:
    master = _FakeMaster(
        [
            _FakeMessage("MC_ROLLRATE_P", None),
            _FakeMessage("MC_ROLLRATE_P", 0.18),
        ]
    )
    assert set_parameter(master, "MC_ROLLRATE_P", 0.18, timeout_s=0.01) is True
