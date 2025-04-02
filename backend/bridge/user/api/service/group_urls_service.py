from rest_framework import status
from rest_framework.request import Request
from user.models import AuthGroupUrls
from web.models import AuthAgencyUsers
from user.api.serializer.group_urls_serializer import GroupUrlsSerializer
from bridge.utils.response_formatter import ResponseFormatter

"""
The rule of Reponse Body structure:
{
    "success"(boolean): if client get response successful or not
    "message"(string):  message detail
    "data"(any): return data
}

"""

class GroupUrlsService:
    serializer_class = GroupUrlsSerializer

    def __init__(self):
        pass

    
    def get_path_element_by_group(self, request: Request):

        try:
            # get user's groups
            user_groups = request.user.groups.all()
            print("User's group is: ", user_groups)
            
            # Get group's name
            group_name = user_groups.first().name if user_groups.exists() else "UnknownGroup"

            # Search the url object result related to specific user group
            group_url_results = AuthGroupUrls.objects.filter(group__in=user_groups).select_related('url')


            # format json
            # get url list of group
            links = list()

            for group_url_result in group_url_results:
                print(group_url_result)
                record = dict()
                record["title"] = group_url_result.url.name
                record["path"] = group_url_result.url.path
                record["element"] = group_url_result.url.element
                links.append(record)

            # get agency's base64
            # 取得該使用者所屬的第一個單位
            user_agency = AuthAgencyUsers.objects.filter(user=request.user).first()
            if (user_agency):
                agency_base64 = user_agency.agency.base64
            else:
                raise ValueError("Invalid user!! Please check account settings")

            
            data = dict()
            data["group"] = group_name
            data["base64"] = agency_base64
            data["links"] = links

            # Serialize data
            serializer = self.serializer_class(data= data)
            # print(serializer.data)
            if serializer.is_valid():
                json = ResponseFormatter.format_get_response(serializer.data)
            else:
                # raise ValueError("wrong type!")
                json = ResponseFormatter.format_400_response(serializer.errors)
            

        except Exception as e:
            print(e)
            json = ResponseFormatter.format_500_response()

        finally:

            return json
        