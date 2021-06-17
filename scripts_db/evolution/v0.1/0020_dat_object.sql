
select 
    til_id
into
    @trap_tileset
from
    tileset
where
    til_name = 'trap';


insert into
    object
        (
        obj_name,
        obj_type,
        obj_til_xid,
        obj_til_x,
        obj_til_y,
        obj_description
        )
    values
        (
        'hole',
        'trap',
        @trap_tileset,
        0,
        0,
        'It is a impassable hole.'
        );

commit;
