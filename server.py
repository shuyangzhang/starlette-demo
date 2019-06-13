from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.endpoints import HTTPEndpoint
import uvicorn
import datetime
import random
import uuid
import aiofiles
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware

app = Starlette(debug=True)
app.mount("/static", StaticFiles(directory="static"))
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.route("/test")
class TestEndpoint(HTTPEndpoint):
	async def get(self, request):
		param1 = request.query_params["param1"]
		param2 = request.query_params["param2"]
		time = str(datetime.datetime.now())
		response_dict = {
			"param1": param1,
			"param2": param2,
			"time": time,
			"random_num": random.randint(1,100000) 
		}
		# response_dict = {"hello": "world"}
		return JSONResponse(response_dict)

@app.route("/upload")
class FileEndpoint(HTTPEndpoint):
	async def post(self, request):
		form = await request.form()
		contents = await form["upload_file"].read()
		saved_file_name = str(uuid.uuid4())
		async with aiofiles.open(f'static/{saved_file_name}', mode="wb") as f:
			await f.write(contents)
		response_dict = {
			"file_name": saved_file_name
		}
		return JSONResponse(response_dict)


if __name__ == "__main__":
	uvicorn.run(app, host="0.0.0.0", port=9009)
