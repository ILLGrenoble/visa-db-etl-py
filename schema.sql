create sequence if not exists flavour_id_seq;

create sequence if not exists flavour_limit_id_seq;

create sequence if not exists image_id_seq;

create sequence if not exists instance_authentication_token_id_seq;

create sequence if not exists instance_command_id_seq;

create sequence if not exists instance_id_seq;

create sequence if not exists instance_member_id_seq;

create sequence if not exists instance_session_id_seq;

create sequence if not exists protocol_id_seq;

create sequence if not exists role_id_seq;

create sequence if not exists instance_attribute_id_seq;

create table if not exists configuration
(
    id    bigserial     not null
        constraint configuration_pkey
            primary key,
    key   varchar(256)  not null,
    value varchar(8192) not null
);

create table if not exists cycle
(
    id         bigint       not null
        constraint cycle_pkey
            primary key,
    end_date   timestamp    not null,
    name       varchar(100) not null,
    start_date timestamp    not null
);

create table if not exists employer
(
    id           bigint not null
        constraint employer_pkey
            primary key,
    country_code varchar(10),
    name         varchar(200),
    town         varchar(100)
);

create table if not exists flavour
(
    id          bigint default nextval('flavour_id_seq'::regclass) not null
        constraint flavour_pkey
            primary key,
    created_at  timestamp                                          not null,
    updated_at  timestamp                                          not null,
    compute_id  varchar(250)                                       not null,
    cpu         real                                               not null,
    deleted     boolean                                            not null,
    memory      integer                                            not null,
    name        varchar(250)                                       not null,
    description varchar(2500)
);

create table if not exists flavour_limit
(
    id          bigint default nextval('flavour_limit_id_seq'::regclass) not null
        constraint flavour_limit_pkey
            primary key,
    object_id   bigint                                                   not null,
    object_type varchar(255)                                             not null,
    flavour_id  bigint                                                   not null
        constraint fk_flavour_id
            references flavour
);

create table if not exists image
(
    id           bigint default nextval('image_id_seq'::regclass) not null
        constraint image_pkey
            primary key,
    created_at   timestamp                                        not null,
    updated_at   timestamp                                        not null,
    boot_command text,
    compute_id   varchar(250)                                     not null,
    deleted      boolean                                          not null,
    description  varchar(2500),
    icon         varchar(100)                                     not null,
    name         varchar(250)                                     not null,
    version      varchar(100),
    visible      boolean                                          not null,
    autologin    varchar(255)
);

create table if not exists instrument
(
    id   bigint       not null
        constraint instrument_pkey
            primary key,
    name varchar(250) not null
);

create table if not exists plan
(
    id         bigserial not null
        constraint plan_pkey
            primary key,
    created_at timestamp not null,
    updated_at timestamp not null,
    preset     boolean   not null,
    flavour_id bigint
        constraint fk_flavour_id
            references flavour,
    image_id   bigint
        constraint fk_image_id
            references image
);

create table if not exists instance
(
    id                  bigint       default nextval('instance_id_seq'::regclass) not null
        constraint instance_pkey
            primary key,
    created_at          timestamp                                                 not null,
    updated_at          timestamp                                                 not null,
    comments            varchar(2500),
    compute_id          varchar(250),
    delete_requested    boolean                                                   not null,
    ip_address          varchar(255),
    last_interaction_at timestamp,
    last_seen_at        timestamp,
    name                varchar(250)                                              not null,
    screen_height       integer                                                   not null,
    screen_width        integer                                                   not null,
    state               varchar(50)                                               not null,
    termination_date    timestamp,
    username            varchar(100),
    plan_id             bigint
        constraint fk_plan_id
            references plan,
    deleted_at          timestamp,
    keyboard_layout     varchar(100) default 'en-gb-qwerty'::character varying,
    security_groups     text,
    home_directory      varchar(250)
);

create table if not exists instance_expiration
(
    id              bigserial not null
        constraint instance_expiration_pkey
            primary key,
    created_at      timestamp not null,
    updated_at      timestamp not null,
    expiration_date timestamp not null,
    instance_id     bigint    not null
        constraint uk_instance_expiration_instance_id
            unique
        constraint fk_instance_id
            references instance
);

create table if not exists instance_session
(
    id            bigint default nextval('instance_session_id_seq'::regclass) not null
        constraint instance_session_pkey
            primary key,
    created_at    timestamp                                                   not null,
    updated_at    timestamp                                                   not null,
    connection_id varchar(150)                                                not null,
    current       boolean                                                     not null,
    instance_id   bigint                                                      not null
        constraint fk_instance_id
            references instance
);

create table if not exists instance_thumbnail
(
    id          bigserial not null
        constraint instance_thumbnail_pkey
            primary key,
    created_at  timestamp not null,
    updated_at  timestamp not null,
    data        text      not null,
    instance_id bigint    not null
        constraint uk_instance_thumbnail_instance_id
            unique
        constraint fk_instance_id
            references instance
);

create table if not exists proposal
(
    id         bigint       not null
        constraint proposal_pkey
            primary key,
    identifier varchar(100) not null,
    title      varchar(2000),
    public_at  timestamp,
    summary    varchar(5000)
);

create table if not exists experiment
(
    id            varchar(32) not null
        constraint experiment_pkey
            primary key,
    cycle_id      bigint      not null
        constraint fk_cycle_id
            references cycle,
    instrument_id bigint      not null
        constraint fk_instrument_id
            references instrument,
    proposal_id   bigint      not null
        constraint fk_proposal_id
            references proposal,
    end_date      timestamp,
    start_date    timestamp
);

create table if not exists instance_experiment
(
    instance_id   bigint      not null
        constraint fk_instance_id
            references instance,
    experiment_id varchar(32) not null
        constraint fk_experiment_id
            references experiment,
    constraint instance_experiment_pkey
        primary key (experiment_id, instance_id)
);

create table if not exists protocol
(
    id   bigint default nextval('protocol_id_seq'::regclass) not null
        constraint protocol_pkey
            primary key,
    name varchar(100)                                        not null,
    port integer                                             not null
);

create table if not exists image_protocol
(
    image_id    bigint not null
        constraint fk_image_id
            references image,
    protocol_id bigint not null
        constraint fk_protocol_id
            references protocol
);

create table if not exists role
(
    id          bigint default nextval('role_id_seq'::regclass) not null
        constraint role_pkey
            primary key,
    description varchar(250),
    name        varchar(100)                                    not null
        constraint uk_role_name
            unique
);

create table if not exists security_group
(
    id   bigserial    not null
        constraint security_group_pkey
            primary key,
    name varchar(250) not null
);

create table if not exists security_group_filter
(
    id                bigserial    not null
        constraint security_group_filter_pkey
            primary key,
    object_id         bigint       not null,
    object_type       varchar(255) not null,
    security_group_id bigint       not null
        constraint fk_security_group_id
            references security_group
);

create table if not exists system_notification
(
    id         bigserial     not null
        constraint system_notification_pkey
            primary key,
    created_at timestamp     not null,
    updated_at timestamp     not null,
    level      varchar(50)   not null,
    message    varchar(4096) not null
);

create table if not exists users
(
    id             varchar(250) not null
        constraint users_pkey
            primary key,
    email          varchar(100),
    first_name     varchar(100),
    instance_quota integer      not null,
    last_name      varchar(100) not null,
    last_seen_at   timestamp,
    affiliation_id bigint
        constraint fk_employer_id
            references employer,
    activated_at   timestamp,
    activated      timestamp
);

create table if not exists experiment_user
(
    experiment_id varchar(32)  not null
        constraint fk_experiment_id
            references experiment,
    user_id       varchar(250) not null
        constraint fk_users_id
            references users,
    constraint experiment_user_pkey
        primary key (experiment_id, user_id)
);

create table if not exists instance_authentication_token
(
    id          bigint default nextval('instance_authentication_token_id_seq'::regclass) not null
        constraint instance_authentication_token_pkey
            primary key,
    created_at  timestamp                                                                not null,
    updated_at  timestamp                                                                not null,
    token       varchar(250)                                                             not null,
    instance_id bigint                                                                   not null
        constraint fk_instance_id
            references instance,
    user_id     varchar(250)                                                             not null
        constraint fk_users_id
            references users
);

create table if not exists instance_command
(
    id          bigint default nextval('instance_command_id_seq'::regclass) not null
        constraint instance_command_pkey
            primary key,
    created_at  timestamp                                                   not null,
    updated_at  timestamp                                                   not null,
    action_type varchar(50)                                                 not null,
    message     varchar(255),
    state       varchar(50)                                                 not null,
    instance_id bigint                                                      not null
        constraint fk_instance_id
            references instance,
    user_id     varchar(250)
        constraint fk_users_id
            references users
);

create table if not exists instance_jupyter_session
(
    id          bigserial    not null
        constraint instance_jupyter_session_pkey
            primary key,
    created_at  timestamp    not null,
    updated_at  timestamp    not null,
    active      boolean      not null,
    kernel_id   varchar(150) not null,
    session_id  varchar(150) not null,
    instance_id bigint       not null
        constraint fk_instance_id
            references instance,
    user_id     varchar(250) not null
        constraint fk_users_id
            references users
);

create table if not exists instance_member
(
    id          bigint default nextval('instance_member_id_seq'::regclass) not null
        constraint instance_member_pkey
            primary key,
    created_at  timestamp                                                  not null,
    updated_at  timestamp                                                  not null,
    role        varchar(255)                                               not null,
    user_id     varchar(250)                                               not null
        constraint fk_users_id
            references users,
    instance_id bigint                                                     not null
        constraint fk_instance_id
            references instance
);

create table if not exists instance_session_member
(
    id                  bigserial    not null
        constraint instance_session_member_pkey
            primary key,
    created_at          timestamp    not null,
    updated_at          timestamp    not null,
    active              boolean      not null,
    last_interaction_at timestamp,
    last_seen_at        timestamp,
    role                varchar(150) not null,
    session_id          varchar(150) not null,
    instance_session_id bigint       not null
        constraint fk_instance_session_id
            references instance_session,
    user_id             varchar(250) not null
        constraint fk_users_id
            references users
);

create table if not exists instrument_scientist
(
    instrument_id bigint       not null
        constraint fk_instrument_id
            references instrument,
    user_id       varchar(250) not null
        constraint fk_users_id
            references users,
    constraint instrument_responsible_pkey
        primary key (instrument_id, user_id)
);

create table if not exists user_role
(
    user_id varchar(250) not null
        constraint fk_users_id
            references users,
    role_id bigint       not null
        constraint fk_role_id
            references role
);

create table if not exists instance_attribute
(
    id          bigint default nextval('instance_attribute_id_seq'::regclass) not null
        constraint instance_attribute_pkey
            primary key,
    created_at  timestamp                                                     not null,
    updated_at  timestamp                                                     not null,
    name        varchar(255)                                                  not null,
    value       varchar(255)                                                  not null,
    instance_id bigint                                                        not null
        constraint fk_instance_id
            references instance
);

