from rest_framework.response import Response
from rest_framework import status

class ReturnResponse:
    @staticmethod
    def to_camel_case(snake_str):
        parts = snake_str.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

    @staticmethod
    def convert_keys_to_camel_case(obj):
        if isinstance(obj, dict):
            return {
                ReturnResponse.to_camel_case(k): ReturnResponse.convert_keys_to_camel_case(v)
                for k, v in obj.items()
            }
        elif isinstance(obj, list):
            return [ReturnResponse.convert_keys_to_camel_case(item) for item in obj]
        else:
            return obj
    @staticmethod     
    def CustomResponse(data,status):
        return Response({"data":data},status=status)
    @staticmethod     
    def CreateSuccess(data="Success"):
        return Response({"data":data},status=status.HTTP_201_CREATED)
    @staticmethod
    def ImportSuccess(data="Success"):
        return Response({"data":data},status=status.HTTP_201_CREATED)
    @staticmethod
    def ImportFail(e="Invalid data for import"):
        return Response({"data":e},status=status.HTTP_400_BAD_REQUEST)
    @staticmethod     
    def CreateFail(e):
        return Response({"data":e},status=status.HTTP_400_BAD_REQUEST)
    @staticmethod
    def RequestFailed(e="You need to wait one day before making another request"):
        return Response({"data":e},status=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod     
    def UpdateSuccess(data="Success"):
        return Response({"data":data},status=status.HTTP_200_OK)
    @staticmethod
    def RedirectRequired(redirectData):
        return Response({"data":redirectData},status=status.HTTP_307_TEMPORARY_REDIRECT)        
    @staticmethod
    def ShowQuizFails():
        return Response({"data":"Quiz Fails"},status=status.HTTP_200_OK)
    @staticmethod     
    def UpdateFail(e="Invalid data for update"):
        return Response({"data":e},status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def DeleteSuccess():
        return Response({"data":"Delte Success"},status=status.HTTP_200_OK)
    
    @staticmethod
    def GetSuccess(data, convert_camel=True):
        if convert_camel:
            data = ReturnResponse.convert_keys_to_camel_case(data)
        return Response({"data": data}, status=status.HTTP_200_OK)

    @staticmethod
    def GetFail(e="Couldn't obtain your request"):
        return Response({"data":e},status=status.HTTP_200_OK)
    @staticmethod
    def EmptyData(e="No data found"):
        return Response({"data":e},status=status.HTTP_404_NOT_FOUND)
