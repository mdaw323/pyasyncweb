import asyncio
import random

import uvicorn
from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse

app = Starlette(debug=True)

@app.route("/rates", methods=["GET"])
async def list_rates(request):
    return JSONResponse({"symbol" : "EUR/PLN", "bid" : 4.2211, "ask" : 4.2322})
    

@app.websocket_route('/ws')
async def websocket_endpoint(websocket):
    await websocket.accept()    
    while True:
        await asyncio.sleep(1)        
        await websocket.send_text("{0:.4f}".format(4.25 + 0.01 * random.random()))
    await websocket.close()
 

@app.route("/streaming", methods=["GET"])
def streaming_content(request):
    return HTMLResponse("""
<!DOCTYPE html>
<html>
    <head>
        <title>Kursy</title>
    </head>
    <body>
        <div id='rates'>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws");
            ws.onmessage = function(event) {
                var rates = document.getElementById('rates')
                rates.innerHTML = event.data                
            };

        </script>
    </body>
</html>
""")    


@app.on_event('startup')
def startup():
    print('Ready to serve!')   

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
