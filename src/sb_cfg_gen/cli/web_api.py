import uvicorn


def run():
    uvicorn.run(
        "sb_cfg_gen.app:app",
        host="0.0.0.0",
        port=9988,
        reload=False
    )
    