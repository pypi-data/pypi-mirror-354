import logging
from typing import Any
from kafka_framework import TopicRouter, MessageContext
from ..schemas.user import UserEvent, UserInDB

# Create a router instance
router = TopicRouter()

logger = logging.getLogger(__name__)


class UserHandlers:
    """Handlers for user-related events."""

    def __init__(self, db_client: Any, email_service: Any):
        """Initialize with required dependencies."""
        self.db = db_client
        self.email_service = email_service

    @router.kafka_handler("user.created")
    async def handle_user_created(self, ctx: MessageContext) -> None:
        """Handle user creation events."""
        try:
            event = UserEvent(**ctx.value)
            logger.info(f"Processing user creation: {event.user_id}")

            # In a real app, you would save to database here
            user_data = event.user_data
            user = UserInDB(
                id=event.user_id,
                email=user_data["email"],
                username=user_data["username"],
                hashed_password=user_data["hashed_password"],
                created_at=event.timestamp,
                updated_at=event.timestamp,
            )

            # Save to database
            await self.db.users.insert_one(user.model_dump())

            # Send welcome email (pseudo-code)
            # await self.email_service.send_welcome_email(
            #     to=user.email,
            #     username=user.username
            # )

            logger.info(f"Successfully processed user creation: {event.user_id}")

        except Exception as e:
            logger.error(
                f"Error processing user.created event: {str(e)}", exc_info=True
            )
            raise

    @router.kafka_handler("user.updated", priority=5)
    async def handle_user_updated(self, ctx: MessageContext) -> None:
        """Handle user update events."""
        try:
            event = UserEvent(**ctx.value)
            logger.info(f"Processing user update: {event.user_id}")

            # Update user in database (pseudo-code)
            # await self.db.users.update_one(
            #     {"id": event.user_id},
            #     {"$set": {**event.user_data, "updated_at": datetime.utcnow()}}
            # )

            logger.info(f"Successfully processed user update: {event.user_id}")

        except Exception as e:
            logger.error(
                f"Error processing user.updated event: {str(e)}", exc_info=True
            )
            raise

    @router.kafka_handler("user.deleted")
    async def handle_user_deleted(self, ctx: MessageContext) -> None:
        """Handle user deletion events."""
        try:
            event = UserEvent(**ctx.value)
            logger.info(f"Processing user deletion: {event.user_id}")

            # Soft delete user (pseudo-code)
            # await self.db.users.update_one(
            #     {"id": event.user_id},
            #     {
            #         "$set": {
            #             "is_active": False,
            #             "deleted_at": datetime.utcnow()
            #         }
            #     }
            # )

            # Send goodbye email (pseudo-code)
            # user = await self.db.users.find_one({"id": event.user_id})
            # if user:
            #     await self.email_service.send_goodbye_email(
            #         to=user["email"],
            #         username=user["username"]
            #     )

            logger.info(f"Successfully processed user deletion: {event.user_id}")

        except Exception as e:
            logger.error(
                f"Error processing user.deleted event: {str(e)}", exc_info=True
            )
            raise
