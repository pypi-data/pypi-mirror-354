from typing import Optional
from .status import APIStatus
from utype import Schema


class ResponseSchema(Schema):
    """API response schema supporting both success and error cases."""

    code: APIStatus
    msg: str
    data: Schema | dict

    def __init__(
        self,
        code: APIStatus,
        msg: Optional[str] = None,
        data: Optional[Schema | dict] = None,
    ):
        super().__init__(code=code, msg=msg or code.description, data=data or {})

    @classmethod
    def success(
        cls, msg: Optional[str] = None, data: Optional[Schema | dict] = None
    ) -> "ResponseSchema":
        """Create a successful response."""
        return cls(APIStatus.OK, msg, data)

    @classmethod
    def error(
        cls,
        code: APIStatus,
        msg: Optional[str] = None,
        data: Optional[Schema | dict] = None,
    ) -> "ResponseSchema":
        """Create an error response."""
        return cls(code, msg, data)

    def __repr__(self) -> str:
        return f"Response(code={self.code}, msg={self.msg}, data={self.data})"

