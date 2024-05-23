from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `tool` (
    `name` VARCHAR(255) NOT NULL  PRIMARY KEY,
    `title` VARCHAR(255) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `url` VARCHAR(2047) NOT NULL,
    `last_updated` DATETIME(6) NOT NULL
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
