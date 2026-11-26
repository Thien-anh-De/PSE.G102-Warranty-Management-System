CREATE TABLE users (
    user_id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_users_username
        UNIQUE (username),

    CONSTRAINT chk_users_role
        CHECK (role IN ('ADMIN', 'TECHNICIAN'))
);

CREATE TABLE customers (
    customer_id VARCHAR(36) PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    email VARCHAR(100),
    address VARCHAR(255)
);

CREATE INDEX idx_customers_phone_number
ON customers(phone_number);

CREATE TABLE devices (
    device_id VARCHAR(36) PRIMARY KEY,
    serial_number VARCHAR(100),
    model_name VARCHAR(100) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    purchase_date DATE
);

CREATE INDEX idx_devices_serial_number
ON devices(serial_number);

CREATE INDEX idx_devices_model_name
ON devices(model_name);

