import uvicorn

from sb_cfg_gen.app import app


def main():
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=9988,
        reload=False
    )


if __name__ == "__main__":
    main()
    