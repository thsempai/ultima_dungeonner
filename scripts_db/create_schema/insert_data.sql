-- insert a user (Sempai)

insert into 
    user
        (
        use_nickname,
        use_password
        )
    values
        (
        'sempai',
        ''
        );

commit;

-- récupération de la variable utilisateur

select
    use_id
into
    @me
from 
    user
where
    use_nickname = 'sempai';

-- insert tileset

insert into
    tileset
        (
        til_name,
        til_path,
        til_type
        )
    values
        (
        'room',
        'img/tileset/dungeon.png',
        'room'
        ),
        (
        'trap',
        'img/tileset/object.png',
        'item'
        );

commit;

-- récupération des variables des tilesets

select 
    til_id
into
    @tilset_object_id
from
    tileset
where
    til_name = 'trap';

select 
    til_id
into
    @tilset_room_id
from
    tileset
where
    til_name = 'room';


-- insert object

insert into
    object
        (
        obj_name,
        obj_til_xid,
        obj_til_x,
        obj_til_y
        )
    values
        (
        'poison trap',
        @tilset_object_id,
        0,
        1
        );

commit;

-- récupération des object

select 
    obj_id
into
    @poison_trap_id
from
    object
where
    obj_name = 'poison trap';


-- insert room

insert into
    room
        (
        roo_name,
        roo_til_xid,
        roo_use_xid
        )
    values
        (
        'first_room',
        @tilset_room_id,
        @me
        );

-- récupération de l'id de la pièce

select
    max(roo_id)
into
    @room_id 
from
    room;

-- insert des objets dans la pièce.

insert into
    room_object
        (
        rob_roo_xid,
        rob_obj_xid,
        rob_x,
        rob_y
        )
    values
        (
        @room_id,
        @poison_trap_id,
        1,
        1
        ),
        (
        @room_id,
        @poison_trap_id,
        10,
        12
        ),
        (
        @room_id,
        @poison_trap_id,
        5,
        10
        );

commit;