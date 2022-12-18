import schemas
import models
import utils


@utils.trace_it_sync(tag="mapper", value="to schema")
def mapping_model_schema(user: models.User) -> schemas.User:
    return schemas.User(
        user_uuid=user.user_uuid,
        username=user.username,
        email=user.email,
        password=user.password
    )


@utils.trace_it_sync(tag="mapper", value="to model")
def mapping_schema_model(user: schemas) -> models.User:
    return models.User(
        user_uuid=user.user_uuid,
        username=user.username,
        email=user.email,
        password=user.password
    )
