from datetime import date

from fastapi import FastAPI
import uvicorn



def main():
    print("Hello from uv-dependencie-demo!")
    print(date.today())

app = FastAPI()
@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    main()
    uvicorn.run(app)

