drop table if exists videos;
drop type if exists video_status;

create type video_status as enum ('new', 'transcoded', 'recognized');

create table videos (
    id serial primary key,
    video_path varchar(255),
    start_time timestamp,
    duration integer,
    camera_number integer,
    location varchar(255),
    status video_status default 'new',
    created_at timestamp default current_timestamp
);


insert into videos
(video_path, start_time, duration, camera_number, location, status)
values ('/test/path/to/video', '2026-01-01 12:00:00', 10, 101, 'test_location', 'new');
