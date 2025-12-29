"""Arithmetic calculation tools."""
from typing import Dict, Literal, Union
from langchain.tools import tool

@tool
async def calculator(
    first_num: float,
    second_num: float,
    operation: Literal["add", "sub", "mul", "div"]
) -> Dict[str, Union[float, str]]:
    """🧮 Arithmetic Calculator Tool"""
    operations = {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
        "div": lambda a, b: a / b if b != 0 else None
    }
    
    try:
        if operation not in operations:
            return {"error": f"Unsupported operation: {operation}"}
        result = operations[operation](first_num, second_num)
        if result is None:
            return {"error": "Division by zero is not allowed"}
        return {"result": result}
    except Exception as e:
        return {"error": f"Calculation failed: {str(e)}"}

@tool
async def percentage_calc(
    value: float,
    percent: float,
    operation: Literal["increase", "decrease"]
) -> Dict[str, Union[float, str]]:
    """📈 Percentage Calculator"""
    try:
        multiplier = 1 + (percent / 100) if operation == "increase" else 1 - (percent / 100)
        return {"result": value * multiplier}
    except Exception as e:
        return {"error": f"Calculation failed: {str(e)}"}

