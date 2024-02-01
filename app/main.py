import logging
import os
import sys

import arango
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
templates = Jinja2Templates(directory="../templates")


class TraversalFormData(BaseModel):
    """ Validate request data """
    idField: str
    maxDepth: int
    bfsDirection: str
    searchID: str


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get('/about')
async def about(request: Request):
    logging.info('about')
    return templates.TemplateResponse("about.html", context={"request": request})


@app.post("/get_graph")
async def get_graph(traversal: TraversalFormData):
    """
    Обход графа и компоновка в формат для отрисовки
    :param traversal: Параметры с формы
    :return:
    """
    start_vertex = f'nodes/{traversal.idField}'
    max_depth = traversal.maxDepth
    bfs_direction = traversal.bfsDirection

    # проверка на то, что пользователь существует в базе
    user_exists_query = """
    RETURN LENGTH(FOR user IN nodes FILTER user._id == @user_id LIMIT 1 RETURN true) > 0
    """
    cursor = db.aql.execute(
        user_exists_query,
        bind_vars={
            'user_id': start_vertex,
        }
    )

    if not list(cursor)[0]:
        return JSONResponse(dict())

    # баг с аггрегацией суммы ребер

    query = """
            for u, e in 0..@max_depth {0} @start_vertex edges
                options {{
                    bfs: true,
                    uniqueVertices: 'path',
                    uniqueEdges: 'path',
                }}
                limit 20000
            return distinct {{
                u,
                from: e._from,
                to: e._to,
                amount: e.amount,
                dlk_cob_date: e.dlk_cob_date
            }}
    """.format(bfs_direction)

    cursor = db.aql.execute(
        query,
        bind_vars={
            'max_depth': max_depth,
            'start_vertex': start_vertex,
        }
    )

    net = list(cursor)
    print('total:', len(net))

    nodes = [node['u'] for node in net]
    nodes = list({v['_id']: v for v in nodes}.values())
    nodes = [{'data': node} for node in nodes]

    edges = dict()
    for edge in net[1:]:
        path = edge['from'] + '->' + edge['to']
        if path in edges:
            edges[path]['amount'] += edge['amount']
        else:
            edges[path] = {
                'amount': edge['amount']
            }

    links = []
    for i, (k, v) in enumerate(edges.items()):
        source, target = k.split('->')
        amount = v['amount']
        edge = {
            'id': i,
            'source': source,
            'target': target,
            'amount': amount,
            'directed': True,
        }
        links.append({'data': edge, 'directed': True})

    print('nodes:', len(nodes))
    print('links:', len(links))

    out = {
        'nodes': nodes,
        'edges': links,
    }

    return JSONResponse(out)


if __name__ == '__main__':
    client = arango.ArangoClient()
    db = client.db(name='_system', username='root', password='root')
    logging.info('Connected to DB')
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "80")), log_level="info")
