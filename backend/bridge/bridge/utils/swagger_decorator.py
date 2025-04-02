"""
Using Decorator to utilze function to realize on another function/class 
"""
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

def get_schema(meta_example: dict):
    """
    Return the example schema if API need
    """
    return openapi.Schema(
                type= openapi.TYPE_OBJECT,
                properties= meta_example if meta_example else None,
                required= list(meta_example.keys()) if meta_example else [],  # 所有字段均为必填项
            )

def insert_pic_parameter():
    return  openapi.Parameter(
                    name= "photo",
                    in_= openapi.IN_FORM,
                    type= openapi.TYPE_FILE,
                    description="上傳的圖片",
                    required= False
                )

def get_manual_parameter(meta_example: dict, with_file: bool= False):
    """
    Convert: openai.Schema(dict) 
    into: openai.Parameter(list)
    """
    manual_parameters = list()
    
    # If need to upload file: Add another file to upload 
    if (with_file):
        manual_parameters.append(insert_pic_parameter())


    # Transfer Schema(JSON) to Parameter(Form-data) 
    if (meta_example):
        for key, field in meta_example.items():
            manual_parameters.append(
                openapi.Parameter(
                    name = key,
                    in_= openapi.IN_FORM,
                    type= field.type,
                    description= field.description,
                    example= field.example,
                    default = field.example,
                    required= False
                )
            )

    return manual_parameters
    

    

# SwaggerUI Auto Schema: Use Serializer's Meta class' example attribute to decorate specific view funciton(API) in CBV.
def auto_schema_with_example(serializer_class):

    """
    Use Meta.example's format to represent example of request body on Swagger doc.
    """
    meta_example = getattr(serializer_class.Meta, "example", None)
    def decorator(func):
        return swagger_auto_schema(
            # manual_parameters=[get_JWT()],
            request_body= get_schema(meta_example),
            responses={
                200: openapi.Response(description="Successful response"),
                401: openapi.Response(description="Unauthorized - Invalid or missing token"),
                }
        )(func)

    return decorator


def auto_schema_without_example():
    """
    Don't need to show the example for GET METHOD view(API)
    """
    def decorator(func):
        return swagger_auto_schema(
            # manual_parameters=[
            #     openapi.Parameter(
            #         name="Authorization",  # Header 名稱
            #         in_=openapi.IN_HEADER,  # 指定為 Header
            #         description="JWT Token, 格式: Bearer {your token}",  # 說明
            #         type=openapi.TYPE_STRING,  # 資料型別
            #         required=True,  # 必填
            #     )
            # ],
            responses={
                200: openapi.Response(description="Successful response"),
                401: openapi.Response(description="Unauthorized - Invalid or missing token"),
                },
        )(func)

    return decorator



def auto_schema_with_file_and_example(serializer_class):
    """
    Multipart/form-data: upload file (PDF, JPG etc..) & JSON in one request
    **Note: this decorator only upload ONE picture per request! 
    """
    meta_example = getattr(serializer_class.Meta, "example", None)

    def decorator(func):
        return swagger_auto_schema(
            manual_parameters= get_manual_parameter(meta_example, with_file= True),
            responses={
                200: openapi.Response(description="Successful response"),
                401: openapi.Response(description="Unauthorized - Invalid or missing token"),
                }
            )(func)
    
    return decorator
    


def get_JWT():
    """
    Return the JWT form-data format for user to access every API if it's needed
    """

    return  openapi.Parameter(
                name="Authorization",  # Header 名稱
                in_=openapi.IN_HEADER,  # 指定為 Header
                description="JWT Token, 格式: Bearer {your token}",  # 說明
                type=openapi.TYPE_STRING,  # 資料型別
                required=True,  # 必填
                )


def auto_schema_without_JWT(serializer_class):

    """
    Only Provided the example, don't use JWT
    """
    meta_example = getattr(serializer_class.Meta, "example", None)
    def decorator(func):
        return swagger_auto_schema(
            request_body= get_schema(meta_example),
            responses={
                200: openapi.Response(description="Successful response"),
                401: openapi.Response(description="Unauthorized - Invalid or missing token"),
                },
        )(func)

    return decorator


def auto_schema_with_query_params(serializer_class):
    """
    Provide only query parameters on GET method
    """
    meta_query_params = getattr(serializer_class.Meta, "query_params", None)

    def decorator(func):
        return swagger_auto_schema(
            manual_parameters= meta_query_params,
            responses={
                200: openapi.Response(description="Successful response"),
                401: openapi.Response(description="Unauthorized - Invalid or missing token"),
                }
            )(func)
    
    return decorator
    