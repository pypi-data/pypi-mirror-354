"""Views for the crypto Extension."""

from typing import TYPE_CHECKING, Any, Dict, Tuple

if TYPE_CHECKING:
    from kozmoai_charting.core.kozmoai_figure import (
        KozmoAIFigure,
    )


class CryptoViews:
    """Crypto Views."""

    @staticmethod
    def crypto_price_historical(  # noqa: PLR0912
        **kwargs,
    ) -> Tuple["KozmoAIFigure", Dict[str, Any]]:
        """Crypto Price Historical Chart."""
        # pylint: disable=import-outside-toplevel
        from kozmoai_charting.charts.price_historical import price_historical

        return price_historical(**kwargs)
