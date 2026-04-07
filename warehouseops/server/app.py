from openenv.core.env_server.http_server import create_app

try:
    from ..models import WarehouseopsAction, WarehouseopsObservation
    from .warehouseops_environment import WarehouseopsEnvironment
except (ImportError, ModuleNotFoundError):
    from models import WarehouseopsAction, WarehouseopsObservation
    from server.warehouseops_environment import WarehouseopsEnvironment

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
