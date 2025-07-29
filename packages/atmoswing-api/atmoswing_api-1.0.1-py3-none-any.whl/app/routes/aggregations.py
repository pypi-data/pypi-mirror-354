import logging
from functools import lru_cache
from fastapi import APIRouter, HTTPException, Depends, Query

from atmoswing_api import config
from atmoswing_api.cache import *
from atmoswing_api.app.models.models import *
from atmoswing_api.app.services.aggregations import *

router = APIRouter()
debug = False


@lru_cache
def get_settings():
    return config.Settings()


# Helper function to handle requests and catch exceptions
async def _handle_request(func, settings: config.Settings, region: str, **kwargs):
    try:
        result = await func(settings.data_dir, region, **kwargs)
        if debug:
            logging.info(f"Result from {func.__name__}: {result}")
        if result is None:
            raise ValueError("The result is None")
        return result
    except FileNotFoundError as e:
        logging.error(f"Files not found for region: {region} "
                      f"(directory: {settings.data_dir})")
        logging.error(f"Error details: {e}")
        raise HTTPException(status_code=400, detail=f"Region or forecast not found ({e})")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error ({e})")


@redis_cache(ttl=3600)
@router.get("/{region}/{forecast_date}/{method}/{lead_time}/entities-values-percentile/{percentile}",
            summary="Analog values for a given region, forecast_date, method, "
                    "lead time, and percentile, aggregated by selecting the "
                    "relevant configuration per entity",
            response_model=EntitiesValuesPercentileAggregationResponse,
            response_model_exclude_none=True)
async def entities_analog_values_percentile(
        region: str,
        forecast_date: str,
        method: str,
        lead_time: int|str,
        percentile: int,
        settings: Annotated[config.Settings, Depends(get_settings)],
        normalize: int = Query(10)):
    """
    Get the analog dates for a given region, forecast_date, method, configuration, and lead_time.
    """
    return await _handle_request(get_entities_analog_values_percentile, settings,
                                 region, forecast_date=forecast_date, method=method,
                                 lead_time=lead_time, percentile=percentile,
                                 normalize=normalize)


@redis_cache(ttl=3600)
@router.get("/{region}/{forecast_date}/series-synthesis-per-method/{percentile}",
            summary="Largest values for a given region, forecast_date, method, "
                    "and percentile, aggregated by selecting the largest values for "
                    "the relevant configurations per entity",
            response_model=SeriesSynthesisPerMethodListResponse,
            response_model_exclude_none=True)
async def series_synthesis_per_method(
        region: str,
        forecast_date: str,
        percentile: int,
        settings: Annotated[config.Settings, Depends(get_settings)],
        normalize: int = Query(10)):
    """
    Get the largest analog values for a given region, forecast_date, and percentile.
    """
    return await _handle_request(get_series_synthesis_per_method, settings,
                                 region, forecast_date=forecast_date,
                                 percentile=percentile, normalize=normalize)


@redis_cache(ttl=3600)
@router.get("/{region}/{forecast_date}/series-synthesis-total/{percentile}",
            summary="Largest values for a given region, forecast_date, "
                    "and percentile, aggregated by time steps",
            response_model=SeriesSynthesisTotalListResponse,
            response_model_exclude_none=True)
async def series_synthesis_total(
        region: str,
        forecast_date: str,
        percentile: int,
        settings: Annotated[config.Settings, Depends(get_settings)],
        normalize: int = Query(10)):
    """
    Get the largest analog values for a given region, forecast_date, and percentile.
    """
    return await _handle_request(get_series_synthesis_total, settings,
                                 region, forecast_date=forecast_date,
                                 percentile=percentile, normalize=normalize)