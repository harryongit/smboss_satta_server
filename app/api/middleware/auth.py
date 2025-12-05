from fastapi import Request, HTTPException, status


async def ensure_authenticated(request: Request):
    if not request.state.user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

