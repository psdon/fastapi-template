"""
1. Business logic only with dependency to repository service.
2. Session object should use dependency injection to ease unit testing.
3. Should not raise Exception related to a web framework (i.e. FastAPI HTTPException), let the api folder handle that.
4. function parameters should be flat, no type hinting based on Pydantic Schema for example
"""
