"""Runtime patches for third-party libraries."""
import logging
logger = logging.getLogger(__name__)

def apply_aiosqlite_patch() -> None:
    try:
        import aiosqlite.core
        if not hasattr(aiosqlite.core.Connection, 'is_alive'):
            def is_alive(self):
                return self._connection is not None
            aiosqlite.core.Connection.is_alive = is_alive
            logger.info("✓ Applied is_alive() patch to aiosqlite.Connection")
    except Exception as e:
        logger.warning(f"Could not apply aiosqlite patch: {e}")