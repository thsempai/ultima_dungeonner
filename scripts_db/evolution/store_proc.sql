-- function get_user

drop function if exists get_user;

delimiter //

create function get_user (nickname varchar(45))
    returns int
    begin

    declare user_id int;

    if not exists(select use_id from user where use_nickname = nickname) then

        insert into
            user
                (
                use_nickname,
                use_password,
                use_creation
                )
            values
                (
                nickname,
                '',
                curdate()
                );
    end if;

    select 
        use_id 
    into 
        user_id
    from 
        user 
    where 
        use_nickname = nickname;

    return user_id;
    end//

delimiter ;

-- function get_dungeon

drop function if exists get_dungeon;

delimiter //


create function get_dungeon (nickname varchar(45)) 
    returns int
    begin

        declare dungeon_id int;
        declare user_id int;

        -- get user id

        select 
            get_user(use_nickname)
        into
            user_id;

        return 1;

    end//

delimiter ;