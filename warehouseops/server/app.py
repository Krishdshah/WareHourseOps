from openenv.core.env_server.http_server import create_app

try:
    # Try package-style first (local dev)
    from warehouseops.models import WarehouseopsAction, WarehouseopsObservation
    from warehouseops.server.warehouseops_environment import WarehouseopsEnvironment
except (ImportError, ModuleNotFoundError):
    try:
        # Try relative paths
        from ..models import WarehouseopsAction, WarehouseopsObservation
        from .warehouseops_environment import WarehouseopsEnvironment
    except (ImportError, ValueError, ModuleNotFoundError):
        # Try flat structure (server as root)
        import models
        from server.warehouseops_environment import WarehouseopsEnvironment
        WarehouseopsAction = models.WarehouseopsAction
        WarehouseopsObservation = models.WarehouseopsObservation

app = create_app(
    WarehouseopsEnvironment,
    WarehouseopsAction,
    WarehouseopsObservation,
    env_name="warehouseops",
)


def main(host: str = "0.0.0.0", port: int = 8000):
    import uvicorn
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
