from loguru import logger

class SoftAssert:
    _failures = []

    @classmethod
    def expect(cls, condition: bool, msg: str = ""):
        if not condition:
            message = msg or "Soft assertion failed"
            cls._failures.append(message)
            logger.error(f"SoftAssert failed: {message}")
        else:
            logger.debug("SoftAssert passed.")
        return cls

    @classmethod
    def verify(cls):
        if cls._failures:
            failure_messages = "\n".join(f"- {msg}" for msg in cls._failures)
            logger.error(f"SoftAssert summary failures:\n{failure_messages}")
            cls._failures.clear()
            raise AssertionError(f"Soft assertion(s) failed:\n{failure_messages}")
        cls._failures.clear()
        return cls

    @classmethod
    def clear(cls):
        cls._failures.clear()
        return cls

# 方便用户直接 import expect
expect = SoftAssert.expect
