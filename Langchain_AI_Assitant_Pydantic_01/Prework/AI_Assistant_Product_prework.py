from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel,Field



class JsonSchema(BaseModel):
    productName: str = Field(description="Name of the Product, eg 'Iphone 16 ProMax'")
    productDetails: str = Field(description="Description of the Product, eg 'This is the latest smartphone from Apples, features are ...")
    prouctPrice: float = Field(description="Describes the appoximate price of product in USD. eg '1650' for Apple 16 Pro Max")



jsonparser = JsonOutputParser(pydantic_object=JsonSchema)
format_ins =  jsonparser.get_format_instructions()

print(format_ins)
print("******")
# prompt = "Tell me about Agentic AI vs AI Agents, format instruction - paragraph with bullets"
llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system","You are an helpful Ecommerce site AI query Agent. Please follow this format \n{ins}"),
        ("user","I want get details of the Product {input_query}")
    ]
   
)
# prompt.format_messages(ins=format_ins,input_query="LG Washing Machine")

print(prompt)

chain = prompt | llm | jsonparser
response = chain.invoke({"ins":format_ins,"input_query":"LG Washing Machine"})

print("\n\n*********************************")
print(response)
  
 