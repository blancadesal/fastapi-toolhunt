from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `completed_task` ADD `field_id` VARCHAR(80);
        ALTER TABLE `completed_task` ADD `tool_id` VARCHAR(255);
        ALTER TABLE `completed_task` DROP COLUMN `field`;
        ALTER TABLE `completed_task` DROP COLUMN `tool_name`;
        ALTER TABLE `tool` MODIFY COLUMN `last_updated` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6);
        ALTER TABLE `completed_task` ADD CONSTRAINT `fk_complete_field_13aeb922` FOREIGN KEY (`field_id`) REFERENCES `field` (`name`) ON DELETE SET NULL;
        ALTER TABLE `completed_task` ADD CONSTRAINT `fk_complete_tool_cd7f7189` FOREIGN KEY (`tool_id`) REFERENCES `tool` (`name`) ON DELETE SET NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `completed_task` DROP FOREIGN KEY `fk_complete_tool_cd7f7189`;
        ALTER TABLE `completed_task` DROP FOREIGN KEY `fk_complete_field_13aeb922`;
        ALTER TABLE `completed_task` ADD `field` VARCHAR(80) NOT NULL;
        ALTER TABLE `completed_task` ADD `tool_name` VARCHAR(255) NOT NULL;
        ALTER TABLE `completed_task` DROP COLUMN `field_id`;
        ALTER TABLE `completed_task` DROP COLUMN `tool_id`;
        ALTER TABLE `tool` MODIFY COLUMN `last_updated` DATETIME(6) NOT NULL;"""
