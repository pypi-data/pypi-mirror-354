"""Derivatives Router."""

from kozmoai_core.app.router import Router

from kozmoai_derivatives.futures.futures_router import router as futures_router
from kozmoai_derivatives.options.options_router import router as options_router

router = Router(prefix="", description="Derivatives market data.")
router.include_router(options_router)
router.include_router(futures_router)
