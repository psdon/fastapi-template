class NotExistDBError(Exception):
    pass


class UniqueConstraintDBError(Exception):
    pass


class AlreadyExistDBError(Exception):
    pass
