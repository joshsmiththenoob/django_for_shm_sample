class ResponseFormatter:
    @staticmethod
    def format(success: bool, status: int, message: str, data: any = None):
        """
        Format the response in a standard structure.

        Args:
            success (bool): Whether the operation was successful.
            message (str): A message describing the result.
            data (any, optional): Additional data to include in the response.

        Returns:
            dict: A dictionary representing the formatted response.
        """
        return {
            "success": success,
            "status": status,
            "message": message,
            "data": data
        }
    
    @staticmethod
    def format_get_response(data: any = None):
        return ResponseFormatter.format(True, 200, "Get data successfully", data)
    
    @staticmethod
    def format_post_response(data: any = None, with_login: bool = False):
        if (with_login):
            return ResponseFormatter.format(True, 201, "Login successfully", data)
        else:
            return ResponseFormatter.format(True, 201, "Create data successfully", data)

    @staticmethod
    def format_put_response(data: any = None):
        return ResponseFormatter.format(True, 204, "Update data successfully", data)
    
    @staticmethod
    def format_delete_response(data: any = None):
        return ResponseFormatter.format(True, 204, "Delete data successfully", data)
    
    @staticmethod
    def format_400_response(data: any = None):
        return ResponseFormatter.format(False, 400, "Error, Bad Request!", data)
    
    @staticmethod
    def format_500_response(data: any = None):
        return ResponseFormatter.format(False, 500, "Error, Interval Server Error!", data)