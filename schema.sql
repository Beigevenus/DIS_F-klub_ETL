begin;

-- Schema
drop schema if exists f_klub cascade;
create schema f_klub;
set search_path to f_klub;

-- Dimension Tables
create table time(
    time_id int,
    year int,
    quarter int,
    month int,
    day int,
    week_day varchar,
    hour int,
    minute int,
    is_holiday boolean,
    PRIMARY KEY(time_id)
);

create table product(
    product_id int,
    category varchar,
    name varchar,
    price decimal,
    is_active boolean,
    deactivation_date int,
    PRIMARY KEY(product_id),
    FOREIGN KEY(deactivation_date) REFERENCES time(time_id)
);

create table member(
    member_id int,
    is_active boolean,
    PRIMARY KEY(member_id)
);

create table location(
    location_id int,
    name varchar,
    PRIMARY KEY(location_id)
);

-- Fact Tables
create table sales(
    product_id int,
    location_id int,
    member_id int,
    time_id int,
    total_sale decimal,
    PRIMARY KEY(product_id, location_id, member_id, time_id),
    FOREIGN KEY(product_id) REFERENCES product(product_id),
    FOREIGN KEY(location_id) REFERENCES location(location_id),
    FOREIGN KEY(member_id) REFERENCES member(member_id),
    FOREIGN KEY(time_id) REFERENCES time(time_id)
);

create table inventory(
    product_id int,
    location_id int,
    time_id int,
    number_of_units int,
    PRIMARY KEY(product_id, location_id, time_id),
    FOREIGN KEY(product_id) REFERENCES product(product_id),
    FOREIGN KEY(location_id) REFERENCES location(location_id),
    FOREIGN KEY(time_id) REFERENCES time(time_id)
);

commit;