"""
APIResponse

Contains class for representing a response from an OGD API,
as well as utility enums used by the APIResponse class.
"""

# import standard libraries
import json
from enum import IntEnum
from typing import Any, Dict, Optional

# import 3rd-party libraries
from flask import Response

# import OGD libraries
import ogd.core.requests.RequestResult as RequestResult

# Import local files

class RESTType(IntEnum):
    """Simple enumerated type to track type of a REST request.
    """
    GET  = 1
    POST = 2
    PUT  = 3

    def __str__(self):
        """Stringify function for RESTTypes.

        :return: Simple string version of the name of a RESTType
        :rtype: _type_
        """
        match self.value:
            case RESTType.GET:
                return "GET"
            case RESTType.POST:
                return "POST"
            case RESTType.PUT:
                return "PUT"
            case _:
                return "INVALID REST TYPE"

class ResponseStatus(IntEnum):
    """Simple enumerated type to track the status of an API request result.
    """
    NONE    =   1
    SUCCESS = 200
    ERR_REQ = 400
    ERR_SRV = 500

    def __str__(self):
        """Stringify function for ResponseStatus objects.

        :return: Simple string version of the name of a ResponseStatus
        :rtype: _type_
        """
        match self.value:
            case ResponseStatus.NONE:
                return "NONE"
            case ResponseStatus.SUCCESS:
                return "SUCCESS"
            case ResponseStatus.ERR_SRV:
                return "SERVER ERROR"
            case ResponseStatus.ERR_REQ:
                return "REQUEST ERROR"
            case _:
                return "INVALID STATUS TYPE"

class APIResponse:
    def __init__(self, req_type:RESTType, val:Any, msg:str, status:ResponseStatus):
        self._type   : RESTType       = req_type
        self._val    : Dict[str, Any] = val
        self._msg    : str            = msg
        self._status : ResponseStatus = status

    def __str__(self):
        return f"{self.Type.name} request: {self.Status}\n{self.Message}\nValues: {self.Value}"

    @staticmethod
    def Default(req_type:RESTType):
        return APIResponse(
            req_type=req_type,
            val=None,
            msg="",
            status=ResponseStatus.NONE
        )

    @staticmethod
    def FromRequestResult(result:RequestResult.RequestResult, req_type:RESTType):
        _status : ResponseStatus
        match result.Status:
            case RequestResult.ResultStatus.SUCCESS:
                _status = ResponseStatus.SUCCESS 
            case RequestResult.ResultStatus.FAILURE:
                _status = ResponseStatus.ERR_REQ
            case _:
                _status = ResponseStatus.ERR_SRV
        ret_val = APIResponse(req_type=req_type, val=None, msg=result.Message, status=_status)
        return ret_val
    
    @staticmethod
    def FromDict(all_elements:Dict[str, Any]) -> Optional["APIResponse"]:
        ret_val : Optional["APIResponse"] = None

        _type_str   = all_elements.get("type", "NOT FOUND").upper()
        _val_str    = all_elements.get("val", {})
        _msg        = all_elements.get("msg", "NOT FOUND")
        _status_str = all_elements.get("status", "NOT FOUND").upper()
        try:
            _type   = RESTType[_type_str]
            _status = ResponseStatus[_status_str]
            _val    = _val_str if isinstance(_val_str, dict) else json.loads(_val_str)
        except KeyError as err:
            pass
        else:
            ret_val = APIResponse(req_type=_type, val=_val, msg=_msg, status=_status)
        finally:
            return ret_val

    @property
    def Type(self) -> RESTType:
        """Property for the type of REST request

        :return: A RESTType representing the type of REST request
        :rtype: _type_
        """
        return self._type

    @property
    def Value(self) -> Dict[str, Any]:
        """Property for the value of the request result.

        :return: Some value, of any type, returned from the request.
        :rtype: Any
        """
        return self._val
    @Value.setter
    def Value(self, new_val:Dict[str, Any]):
        self._val = new_val


    @property
    def Message(self) -> str:
        """Property for the message associated with a request result.

        :return: A string message giving details on the result of the request.
        :rtype: str
        """
        return self._msg

    @property
    def Status(self) -> ResponseStatus:
        """Property for the status of the request.

        :return: A ResponseStatus indicating whether request is/was successful, incomplete, failed, etc.
        :rtype: ResponseStatus
        """
        return self._status

    @property
    def AsDict(self):
        return {
            "type"   : str(self._type),
            "val"    : json.dumps(self._val),
            "msg"    : self._msg,
            "status" : str(self._status)
        }

    @property
    def AsJSON(self):
        return json.dumps(self.AsDict)

    @property
    def AsFlaskResponse(self) -> Response:
        return Response(response=self.AsJSON, status=self.Status.value, mimetype='application/json')

    def RequestErrored(self, msg:str):
        self._status = ResponseStatus.ERR_REQ
        self._msg = f"ERROR: {msg}"

    def ServerErrored(self, msg:str):
        self._status = ResponseStatus.ERR_SRV
        self._msg = f"SERVER ERROR: {msg}"

    def RequestSucceeded(self, msg:str, val:Any):
        self._status = ResponseStatus.SUCCESS
        self._msg = f"SUCCESS: {msg}"
        self._val = val
