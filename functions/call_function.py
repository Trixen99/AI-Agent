from google.genai import types
from functions.available_functions import function_dictionary
import ast

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    arguments = function_call_part.args
    working_directory = "./calculator"

    if function_name not in function_dictionary:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function = function_dictionary[function_call_part.name]
    
    function_result = function(working_directory, **arguments)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )