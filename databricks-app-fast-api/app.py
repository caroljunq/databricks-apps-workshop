import pandas as pd
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import os
import uvicorn

log = logging.getLogger('uvicorn')
log.setLevel(logging.ERROR)

app = FastAPI()

@app.get('/api', response_class=HTMLResponse)
def hello_world():
    chart_data = pd.DataFrame({'Apps': [x for x in range(30)],
                               'Fun with data': [2 ** x for x in range(30)]})
    return f'<h1>Hello, World!</h1> {chart_data.to_html(index=False)}'

if __name__ == '__main__':
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_RUN_PORT', 8000))
    
    uvicorn.run(app, host=host, port=port)
    print(f"FastAPI app running on http://{host}:{port}")
