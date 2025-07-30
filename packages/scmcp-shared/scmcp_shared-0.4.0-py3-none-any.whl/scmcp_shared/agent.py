import instructor
from openai import OpenAI
from scmcp_shared.schema.tool import ToolList
import os



def select_tool(query):

    API_KEY = os.environ.get("API_KEY",  None)
    BASE_URL = os.environ.get("BASE_URL", None)
    MODEL = os.environ.get("MODEL", None)

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    client = instructor.from_openai(client)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system", 
                "content": f"you are a bioinformatician, you are given a task and a list of tools, you need to select the most directly relevant tools to use to solve the task"},
            {
                "role": "user",
                "content": query
            },  
        ],
        response_model=ToolList,
    )
    return response.tools
