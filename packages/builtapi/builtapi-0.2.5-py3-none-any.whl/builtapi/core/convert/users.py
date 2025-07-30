from typing import Union

from builtapi.core.schemas.users import UserProfile


def user_profile(method):
    """ Validation wrap output from profile endpoint """

    def inner(*args, **kwargs) -> Union[UserProfile, None]:
        profile_info = method(*args, **kwargs)

        if profile_info is None:
            return None
        else:
            return UserProfile(id=profile_info.get('id'), created_at=profile_info.get('createdAt'),
                               updated_at=profile_info.get('updatedAt'), external_id=profile_info.get('externalId'),
                               email=profile_info.get('email'), name=profile_info.get('name'))

    return inner
