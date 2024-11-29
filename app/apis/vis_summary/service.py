import io
import base64
import requests
from bs4 import BeautifulSoup as bs
from graphviz import Digraph
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

from app.core.logger import log_excution_time
from app.core.config import get_settings
from app.apis.vis_summary.schema import VISSUMMARYResponseSchema

import tempfile
import os

class VISSUMMARYService:
    def __init__(self):
        self.settings = get_settings()
        self.summary = self.settings.summary

        self.graph_prompt = f"""Please analyze the following text and create a simple, well-organized mind map. 
        Focus on extracting **key concepts** as nodes and **essential relationships** as edges. 
        Your task is to distill the information to its core elements for a clear and concise graph.

        1. Each <node> represents a significant concept, idea, or topic in the text. 
           - Use a brief, precise name for the node.
           - Provide a **one-sentence description** to summarize the concept.

        2. Each <edge> connects two nodes and describes their relationship clearly, such as:
           - "is related to"
           - "is a part of"
           - "leads to"
           - "depends on"

        3. Use the following **html tag** format to represent nodes and edges:

        <node>
            <name>
                [Node name]
            </name>
            <description>
                [Brief description of the node]
            </description>
        </node>

        <edge>
            <left>
                [Input node name]
            </left>
            <right>
                [Output node name]
            </right>
            <relationship>
                [Relationship type]
            </relationship>
        </edge>

        **Example**:
        <node>
            <name>
                Memory access
            </name>
            <description>
                Accessing and retrieving stored data in memory systems.
            </description>
        </node>

        <edge>
            <left>
                Memory access
            </left>
            <right>
                Sequential access
            </right>
        </edge>

        Ensure the graph remains minimal but comprehensive, capturing only the **most important concepts** and their relationships.
        Nodes and edges and name and description and input and output must be stacked on tags. 
        like <node></node> <edge></edge> <name></name> <description></description> <left></left> <right></right>"""

        self.url = "https://api.hyperbolic.xyz/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.summary.model_key}"
        }

    @log_excution_time
    async def run_vissummary_process(self, text: str):
        split_token_len = 23000
        input_text = text[:split_token_len]

        print(input_text)

        data = {
            "messages": [
                {
                "role": "assistant", 
                "content": f"{self.graph_prompt}"},
                {
                "role": "user",
                "content": f"input_text : {input_text}"
                }
            ],
            "model": f"{self.summary.model_name}",
            "max_tokens": 30000,
            "temperature": 0.7,
            "top_p": 0.9
        }

        response = requests.post(self.url, headers=self.headers, json=data)

        response_text = response.json()['choices'][0]['message']['content']
        dot = Digraph(format="png")
        dot.attr(rankdir="TB", splines="ortho", ranksep="1", nodesep="0.8")

        graph_html = bs(response_text, 'html.parser')

        nodes = graph_html.find_all('node')
        edges = graph_html.find_all('edge')

        for data in nodes:
            node_name = data.find('name').get_text()
            node_desc = data.find('description').get_text()
            node_label = f"{node_name}\n\n{node_desc}"  

            dot.node(
                name=node_name,
                label=node_label,
                shape="box",
                style="rounded, filled",
                fillcolor="lightgrey",
                fontsize="10",
                fontname="Helvetica"
            )

        for data in edges:
            input_node = data.find('left').get_text()
            output_node = data.find('right').get_text()

            dot.edge(input_node, output_node, arrowhead="vee", color="black", penwidth="1.2")

        img_stream = io.BytesIO()
        img_stream.write(dot.pipe(format='png'))

        img_stream.seek(0) 

        return StreamingResponse(img_stream, media_type="image/png")

