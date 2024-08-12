SET SQL_SAFE_UPDATES = 0;
ALTER TABLE tm_db.transfers ADD COLUMN transfer_type_str VARCHAR(50);

UPDATE transfers
SET transfer_type_str = CASE
    WHEN transfer_type = 0 THEN 'Not loan'
    WHEN transfer_type = 1 THEN 'Loan'
    WHEN transfer_type = 2 THEN 'End of loan'
    ELSE 'Unknown'
END;

ALTER TABLE transfers DROP COLUMN transfer_type;
ALTER TABLE transfers CHANGE COLUMN transfer_type_str transfer_type VARCHAR(50);


