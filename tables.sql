create table "cpu"
(
    "cpu_id" serial primary key,
    "name"   varchar(128) unique
);
create table "brand"
(
    "brand_id" serial primary key,
    "name"     varchar(16) unique
);
create table "user"
(
    user_id    serial primary key,
    "email"    varchar(128) unique not null,
    "password" varchar(128)        not null,
    "is_admin" bool default false
);
create table "brand_subscription"
(
    "user_id"  int references "user" (user_id) on delete cascade,
    "brand_id" int references "brand" (brand_id) on delete cascade,
    primary key (user_id, brand_id)
);
create table "chipset"
(
    chipset_id serial primary key,
    "name"     varchar(64) unique
);
create table "gpu"
(
    "gpu_id" serial primary key,
    "name"   varchar(64) unique
);
create table "phone"
(
    phone_id                serial primary key,
    "model"                 varchar(64)                     not null unique,
    "brand_id"              int references brand (brand_id) not null,
    "release"               date,
    "height"                float4,
    "width"                 float4,
    "thickness"             float4,
    "resolution"            varchar(12), -- 1024x720
    "ppi"                   int,
    "cpu_id"                int references cpu (cpu_id),
    "chipset_id"            int references chipset (chipset_id),
    "gpu_id"                int references gpu (gpu_id),
    "memory_card_dedicated" bool,
    "internal_memory"       int4[],
    "ram"                   int4[],
    "wifi"                  varchar(32),
    "sim"                   varchar(128),
    "connector"             varchar(32),
    "audio_jack"            bool,
    "bluetooth_version"     float4,
    "gps"                   bool,
    "nfc"                   bool,
    "radio"                 bool,
    "battery_capacity"      int,
    "battery_removable"     bool,
    "image_url"             varchar(128) -- check length of urls
);

create table "phone_subscription"
(
    "user_id"  int references "user" (user_id) on delete cascade,
    "phone_id" int references "phone" (phone_id) on delete cascade,
    primary key (user_id, phone_id)
);
create table "comment"
(
    comment_id serial primary key,
    "content"  varchar                         not null,
    "score"    int default 0, -- TODO: calculate with a trigger
    "user_id"  int references "user" (user_id) not null,
    "phone_id" int references phone (phone_id) not null
);

create table "user-vote"
(
    user_id    int references "user" (user_id)     not null,
    comment_id int references comment (comment_id) not null,
    primary key (user_id, comment_id)
);



create table "camera"
(
    "camera_id" serial primary key,
    "mp"        int4,
    "f"         float4,
    unique (mp, f)
);


create table "phone-camera"
(
    phone_id  int references phone (phone_id) on delete cascade,
    camera_id int references camera (camera_id) on delete cascade,
    primary key (phone_id, camera_id)
);

insert into "user" (email, password, is_admin) VALUES ('admin@example.com', 'admin', true);