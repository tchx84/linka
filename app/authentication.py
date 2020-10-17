import os
import json


from fastapi import Request, HTTPException, status, Header


tokens = None


def get_all_tokens():
    global tokens

    if tokens is not None:
        return tokens
    try:
        sources_path = os.environ.get('SOURCES_PATH')
        if sources_path is None:
            raise RuntimeError('SOURCES_PATH environment variable is required')
        with open(sources_path) as sources_json:
            tokens = json.load(sources_json)
        return tokens['tokens']
    except KeyError:
        raise RuntimeError('Tokens Property is not present in sources file')
    except IOError:
        raise RuntimeError('SOURCES_PATH environment variable is required')


def get_current_source(request: Request = Header(None)):
    try:
        x_api_key = request.headers['x-api-key']
        tokens = get_all_tokens()
        if (x_api_key):
            source = tokens[x_api_key]
            if (source):
                return source
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect X-Api-Key Token is invalid",
            headers={"WWW-Authenticate": "Basic"},
        )
