-- SQL script that creates a stored procedure `ComputeAverageScoreForUser` that computes and store the average score for a student

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(user_id INT)
BEGIN
		-- declare variables
		DECLARE total_score INT DEFAULT 0;
		DECLARE project_count INT DEFAULT 0;

		-- calculate total score
		SELECT SUM(score) INTO total_score
		FROM corrections
		WHERE corrections.user_id = user_id;

		-- calculate project count
		SELECT COUNT(*) INTO project_count
		FROM corrections
		WHERE corrections.user_id = user_id;

		-- update average score in users table
		UPDATE users
		SET users.average_score = IF(
				project_count = 0,
				0,
				total_score / project_count
		)
		WHERE id = user_id;
END$$
DELIMITER ;
