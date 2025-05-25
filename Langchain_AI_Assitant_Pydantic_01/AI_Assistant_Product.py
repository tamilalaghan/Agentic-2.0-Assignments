from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel,Field
import json


class JsonSchema(BaseModel):
    productName: str = Field(description="Name of the Product, eg 'Iphone 16 ProMax'")
    productDetails: str = Field(description="Description of the Product in max two line, eg 'This is the latest smartphone from Apples, features are ...")
    prouctPrice: int = Field(description="Describes the appoximate price of product in USD. eg '1650' for Apple 16 Pro Max")

class AiInventoryAgent():
    def invokeLCEL(self,query):

        #Define the Model
        llm = ChatOpenAI(model="gpt-4o-mini",
                         temperature=0.3)

        #Define the OutputParser
        customJsonParser = JsonOutputParser(pydantic_object=JsonSchema)

        #Store the fomratInstructions
        format_ins = customJsonParser.get_format_instructions()

        #Define ChatPromptTemplate
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system","You are an helpful Ecommerce site AI query Agent. Please follow this format \n{instructions}"),
                ("user","I want get details of the Product {input_query}")
            ]
        )

        # LCEL Chain
        chain = prompt | llm | customJsonParser

        # Invoke LCEL
        result = chain.invoke({
                        "instructions": format_ins,
                        "input_query":query})
        
        # Print Result
        print("\n********Product Details Follows*********\n")
        print(f"{result}\n\n")
       
        # Format Result
        print("***Formatted Response***")
        print(f"{json.dumps(result, indent=2)}\n")
        



#### Actual Invocations ####
agent = AiInventoryAgent()


print("**** This is an implementation of an AI Inventory Agent ****")
print("Note: Type 'bye' to exit anytime")
while True:
    userQuery = input("\nPlease enter the product name, that you would like to query eg.Samsung Galaxy S25 :  ")
    if(userQuery.lower()=="bye"):
       print("\nHope to see you soon! Bye")
       break
    try :
     agent.invokeLCEL(query=userQuery)
     print("\n Lets continue for more query ")
    except Exception as err:
       print("\n\nSome exception Occured, error message ",err)
       print("\n\nLets Try Again")

  
 