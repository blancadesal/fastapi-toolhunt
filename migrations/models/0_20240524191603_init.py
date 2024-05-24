from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `completed_task` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `tool_name` VARCHAR(255) NOT NULL,
    `tool_title` VARCHAR(255) NOT NULL,
    `field` VARCHAR(80) NOT NULL,
    `user` VARCHAR(255) NOT NULL,
    `completed_date` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `field` (
    `name` VARCHAR(80) NOT NULL  PRIMARY KEY,
    `description` VARCHAR(2047) NOT NULL,
    `input_options` VARCHAR(2047),
    `pattern` VARCHAR(320)
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `tool` (
    `name` VARCHAR(255) NOT NULL  PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `url` VARCHAR(2047) NOT NULL,
    `last_updated` DATETIME(6) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `task` (
    `id` INT NOT NULL  PRIMARY KEY,
    `last_attempted` DATETIME(6),
    `last_updated` DATETIME(6) NOT NULL,
    `field_name_id` VARCHAR(80) NOT NULL,
    `tool_name_id` VARCHAR(255) NOT NULL,
    CONSTRAINT `fk_task_field_f0943fa6` FOREIGN KEY (`field_name_id`) REFERENCES `field` (`name`) ON DELETE CASCADE,
    CONSTRAINT `fk_task_tool_e47144f8` FOREIGN KEY (`tool_name_id`) REFERENCES `tool` (`name`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
