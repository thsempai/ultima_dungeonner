-- insert data_site

insert into
    data_site
        (
        das_field,
        das_data
        )
    values
        (
        'version',
        'alpha v0.1'
        ),
        (
        'release date',
        '01/04/2013'
        );


-- insert update_file

insert into
    update_file
        (
        upf_path,
        upf_update_date
        )
    values
        (
        'img/gui/gui.png',
        curdate()
        );

-- insert a user (Sempai)

insert into 
    user
        (
        use_nickname,
        use_creation,
        use_password
        )
    values
        (
        'Creator',
        curdate(),
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
    use_nickname = 'Creator';

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
        'img/tileset/traps.png',
        'item'
        ),
        (
        'imp',
        'img/tileset/imp.png',
        'enemy'
        ),
        (
        'item',
        'img/tileset/items.png',
        'room'
        )
        ;

commit;

-- récupération des variables des tilesets

select 
    til_id
into
    @tilset_trap_id
from
    tileset
where
    til_name = 'trap';

select 
    til_id
into
    @tilset_obj_id
from
    tileset
where
    til_name = 'item';

select 
    til_id
into
    @tilset_room_id
from
    tileset
where
    til_name = 'room';

select 
    til_id
into
    @tileset_imp_id
from
    tileset
where
    til_name = 'imp';


-- insert object

insert into
    object
        (
        obj_name,
        obj_type,
        obj_til_xid,
        obj_til_x,
        obj_til_y
        )
    values
        (
        'poison trap',
        'trap',
        @tilset_trap_id,
        0,
        1
        ),
        (
        'heal potion',
        'item',
        @tilset_obj_id,
        0,
        0
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

select 
    obj_id
into
    @heal_potion_id
from
    object
where
    obj_name = 'heal potion';


-- insert des enemy

insert
    enemy
        (
        ene_name,
        ene_til_xid,
        ene_til_x,
        ene_til_y
        )
    values
        (
        'imp',
        @tileset_imp_id,
        0,
        0
        );

commit;

-- récupération des objects

select 
    ene_id
into
    @imp_id
from
    enemy
where
    ene_name = 'imp';


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
        ),
        (
        @room_id,
        @heal_potion_id,
        6,
        6
        ),
        (
        @room_id,
        @heal_potion_id,
        7,
        1
        );

-- insert des enemy dans la pièce.

insert into
    room_enemy
        (
        ren_roo_xid,
        ren_ene_xid,
        ren_x,
        ren_y,
        ren_ene_lvl
        )
    values
        (
        @room_id,
        @imp_id,
        3,
        3,
        1
        ),
        (
        @room_id,
        @imp_id,
        10,
        10,
        1
        ),
        (
        @room_id,
        @imp_id,
        5,
        2,
        1
        );

commit;

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
        'second_room',
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
        @heal_potion_id,
        1,
        3
        ),
        (
        @room_id,
        @heal_potion_id,
        6,
        6
        );

-- insert des enemy dans la pièce.

insert into
    room_enemy
        (
        ren_roo_xid,
        ren_ene_xid,
        ren_x,
        ren_y,
        ren_ene_lvl
        )
    values
        (
        @room_id,
        @imp_id,
        10,
        5,
        1
        );

commit;