-- Email validation
-- SQL script that creates a trigger that resets the attribute valid_email only when the email has been changed.

DROP TRIGGER IF EXISTS email_validator;

DELIMITER $$
CREATE TRIGGER email_validator
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
		IF NEW.email != OLD.email THEN
				SET NEW.valid_email = 0;
		END IF;
END$$
DELIMITER ;
