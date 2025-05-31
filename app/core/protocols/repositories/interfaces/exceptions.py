from .generics_types import BaseORMModel


class EntityNotFoundError(Exception):
    """If entity with specific id wasn't found"""

    def __init__(self, model_cls: type[BaseORMModel], id_: int | None, *conditions):
        if id_ is not None:
            super().__init__(
                f"The entity {model_cls.__name__} with id={id_} wasn't found."
            )
        else:
            super().__init__(
                f"The entity {model_cls.__name__} was not found with {' '.join(conditions)}."
            )
        self.model_cls = model_cls
        self.id_ = id_
