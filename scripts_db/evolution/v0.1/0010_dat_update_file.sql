-- mise à jour pour forcer le télécharghement

insert into
    update_file
        (
        upf_path,
        upf_update_date
        )
    values
        (
        'img/tileset/traps.png',
        curdate()
        );

commit;