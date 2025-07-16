def convert_pydantic_to_dict(pydanticModelList) -> list:
    return [ {"role": message.role, "content": message.content} for message in pydanticModelList]