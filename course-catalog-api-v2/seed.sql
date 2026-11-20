-- The Lab 6 database already contains these records. This file is for a new empty database.
INSERT INTO courses (id, title, description, credits, is_elective, likes, level) VALUES
('ai-integration', 'AI Integration', 'Using AI services in web applications.', 5, true, 12, 'beginner'),
('api-design', 'API Design', 'Designing clear and reliable APIs.', 4, false, 8, 'beginner'),
('cloud-basics', 'Cloud Basics', 'Introduction to cloud platforms.', 3, true, 4, 'beginner')
ON CONFLICT (id) DO NOTHING;

INSERT INTO students (name, email) VALUES
('Aigerim', 'aigerim@example.com'),
('Daniyar', 'daniyar@example.com')
ON CONFLICT (email) DO NOTHING;
