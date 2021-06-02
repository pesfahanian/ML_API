import inspect
import logging

from fastapi import Depends

from authentication.methods import authenticate_admin, authenticate_user

logger = logging.getLogger(__name__)


class authentication:
    """
    [Endpoint authentication decorator.]
    """
    def admin_required(func):
        """
        [Sets an admin authentication requirement.]

        Args:
            func ([type]): [Function to be decorated.]
        """
        async def wrapper(
                admin: str = Depends(authenticate_admin), *args, **kwargs):
            logger.info('Admin access granted.')
            return await func(*args, **kwargs)

        # Fix signature of wrapper
        wrapper.__signature__ = inspect.Signature(
            parameters=[
                # Use all parameters from func
                *inspect.signature(func).parameters.values(),
                # Skip *args and **kwargs from wrapper parameters:
                *filter(
                    lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL,
                                             inspect.Parameter.VAR_KEYWORD),
                    inspect.signature(wrapper).parameters.values())
            ],
            return_annotation=inspect.signature(func).return_annotation,
        )
        return wrapper

    def user_required(func):
        """
        [Sets a user authentication requirement.
         User has to exist in the users database and
            have a 'True' active status.]

        Args:
            func ([type]): [Function to be decorated.]
        """
        async def wrapper(
                _user: str = Depends(authenticate_user), *args, **kwargs):
            authentication.user = _user
            logger.info(f'User access granted for user {_user}.')
            return await func(*args, **kwargs)

        # Fix signature of wrapper
        wrapper.__signature__ = inspect.Signature(
            parameters=[
                # Use all parameters from func
                *inspect.signature(func).parameters.values(),
                # Skip *args and **kwargs from wrapper parameters:
                *filter(
                    lambda p: p.kind not in (inspect.Parameter.VAR_POSITIONAL,
                                             inspect.Parameter.VAR_KEYWORD),
                    inspect.signature(wrapper).parameters.values())
            ],
            return_annotation=inspect.signature(func).return_annotation,
        )
        return wrapper
