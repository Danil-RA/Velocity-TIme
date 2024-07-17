from typing import Union
from typing import List, Tuple
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse,StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

app = FastAPI()

app.mount("/static",StaticFiles(directory="static"), name = "static")
templates = Jinja2Templates(directory="templates")


@app.get("/",response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html",{"request": request})

   
@app.post("/process/")
async def process_tup(request: Request):
    form_data = await request.form()
    tuple_str = form_data.get("val")
    tuple_list = tuple_str.split(";")
    x = []
    y = []
    for tup in tuple_list:
        tup = tup.split("(") 
        s = tup[1].split(")")
        a = s[0].split(",")
        x.append(int(a[0]))
        y.append(int(a[1]))
    print(x)
    print(y)
    
    global area
    area = np.trapz(y,x)
    new_area = str(area)
    

    plt.plot(x, y)
    plt.xlabel("Time(s)")
    plt.ylabel("Velocity(m/s)")
    plt.fill_between(x,y,color = "skyblue",alpha = 0.4)
    plt.plot(x,y, color = "slateblue",alpha = 0.6)


    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    global image_data
    image_data = buf

    return templates.TemplateResponse("content.html",{"request" : request, "area":new_area})

@app.get("/process")
async def image():
    return StreamingResponse(image_data, media_type= "image/png")






# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}