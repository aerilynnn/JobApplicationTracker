from fastapi import FastAPI

app = FastAPI(title="Job Tracker API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
