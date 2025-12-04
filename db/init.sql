CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task_text VARCHAR(255) NOT NULL,
    is_done BOOLEAN DEFAULT FALSE
);

INSERT INTO tasks (task_text, is_done) VALUES
('Finish cloud computing homework', FALSE),
('Review three-tier architecture slides', TRUE),
('Practice Docker commands', FALSE);
