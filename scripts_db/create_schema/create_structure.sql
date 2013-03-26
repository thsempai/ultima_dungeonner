SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `1gam201302` ;
CREATE SCHEMA IF NOT EXISTS `1gam201302` DEFAULT CHARACTER SET utf8 ;
USE `1gam201302` ;

-- -----------------------------------------------------
-- Table `1gam201302`.`data_site`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`data_site` (
  `das_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `das_field` VARCHAR(45) NOT NULL ,
  `das_data` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`das_id`) ,
  UNIQUE INDEX `das_field_UNIQUE` (`das_field` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = big5;


-- -----------------------------------------------------
-- Table `1gam201302`.`user`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`user` (
  `use_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `use_nickname` VARCHAR(45) NOT NULL ,
  `use_password` VARCHAR(45) NOT NULL ,
  `use_last_connection` DATETIME NULL DEFAULT NULL ,
  `use_creation` DATETIME NOT NULL ,
  PRIMARY KEY (`use_id`) ,
  UNIQUE INDEX `ndx_use_name` (`use_nickname` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 16
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`dungeon`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`dungeon` (
  `dun_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `dun_date` DATE NULL DEFAULT NULL ,
  `dun_use_xid` INT(11) NOT NULL ,
  PRIMARY KEY (`dun_id`) ,
  INDEX `fk_user_fk2` (`dun_use_xid` ASC) ,
  CONSTRAINT `fk_user_fk2`
    FOREIGN KEY (`dun_use_xid` )
    REFERENCES `1gam201302`.`user` (`use_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`tileset`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`tileset` (
  `til_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `til_name` VARCHAR(45) NOT NULL ,
  `til_path` VARCHAR(100) NOT NULL ,
  `til_type` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`til_id`) )
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`enemy`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`enemy` (
  `ene_id` INT(11) NOT NULL ,
  `ene_name` VARCHAR(45) NOT NULL ,
  `ene_til_xid` INT(11) NOT NULL ,
  `ene_til_x` INT(11) NOT NULL ,
  `ene_til_y` INT(11) NOT NULL ,
  `ene_description` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`ene_id`) ,
  UNIQUE INDEX `ene_name_UNIQUE` (`ene_name` ASC) ,
  INDEX `fk_tileset_fk2` (`ene_til_xid` ASC) ,
  CONSTRAINT `fk_tileset_fk2`
    FOREIGN KEY (`ene_til_xid` )
    REFERENCES `1gam201302`.`tileset` (`til_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`object`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`object` (
  `obj_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `obj_name` VARCHAR(45) NOT NULL ,
  `obj_type` VARCHAR(20) NOT NULL ,
  `obj_til_xid` INT(11) NOT NULL ,
  `obj_til_x` INT(11) NOT NULL ,
  `obj_til_y` INT(11) NOT NULL ,
  `obj_description` VARCHAR(100) NOT NULL ,
  PRIMARY KEY (`obj_id`) ,
  INDEX `fk_tileset_fk` (`obj_til_xid` ASC) ,
  CONSTRAINT `fk_tileset_fk`
    FOREIGN KEY (`obj_til_xid` )
    REFERENCES `1gam201302`.`tileset` (`til_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`room`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`room` (
  `roo_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `roo_name` VARCHAR(100) NOT NULL ,
  `roo_use_xid` INT(11) NOT NULL ,
  `roo_til_xid` INT(11) NOT NULL ,
  PRIMARY KEY (`roo_id`) ,
  UNIQUE INDEX `ndx_roo_name` (`roo_name` ASC) ,
  INDEX `fk_user_fk1` (`roo_use_xid` ASC) ,
  INDEX `fk_tileset_fk1` (`roo_til_xid` ASC) ,
  CONSTRAINT `fk_tileset_fk1`
    FOREIGN KEY (`roo_til_xid` )
    REFERENCES `1gam201302`.`tileset` (`til_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_fk1`
    FOREIGN KEY (`roo_use_xid` )
    REFERENCES `1gam201302`.`user` (`use_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`room_dungeon`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`room_dungeon` (
  `rod_roo_xid` INT(11) NOT NULL AUTO_INCREMENT ,
  `rod_dun_xid` INT(11) NOT NULL ,
  PRIMARY KEY (`rod_roo_xid`, `rod_dun_xid`) ,
  INDEX `fk_dungeon_fk1` (`rod_dun_xid` ASC) ,
  INDEX `fk_room_fk1` (`rod_roo_xid` ASC) ,
  CONSTRAINT `fk_dungeon_fk1`
    FOREIGN KEY (`rod_dun_xid` )
    REFERENCES `1gam201302`.`dungeon` (`dun_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_room_fk1`
    FOREIGN KEY (`rod_roo_xid` )
    REFERENCES `1gam201302`.`room` (`roo_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`room_enemy`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`room_enemy` (
  `ren_roo_xid` INT(11) NOT NULL ,
  `ren_x` INT(11) NOT NULL ,
  `ren_y` INT(11) NOT NULL ,
  `ren_ene_xid` INT(11) NOT NULL ,
  `ren_ene_lvl` INT(11) NOT NULL ,
  PRIMARY KEY (`ren_roo_xid`, `ren_x`, `ren_y`) ,
  INDEX `fk_room_fk2` (`ren_roo_xid` ASC) ,
  INDEX `fk_enemy_fk1` (`ren_ene_xid` ASC) ,
  CONSTRAINT `fk_room_fk2`
    FOREIGN KEY (`ren_roo_xid` )
    REFERENCES `1gam201302`.`room` (`roo_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_enemy_fk1`
    FOREIGN KEY (`ren_ene_xid` )
    REFERENCES `1gam201302`.`enemy` (`ene_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`room_object`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`room_object` (
  `rob_roo_xid` INT(11) NOT NULL ,
  `rob_x` INT(11) NOT NULL ,
  `rob_y` INT(11) NOT NULL ,
  `rob_obj_xid` INT(11) NOT NULL ,
  PRIMARY KEY (`rob_roo_xid`, `rob_x`, `rob_y`) ,
  INDEX `fk_object_fk1` (`rob_obj_xid` ASC) ,
  INDEX `fk_room_fk` (`rob_roo_xid` ASC) ,
  CONSTRAINT `fk_object_fk1`
    FOREIGN KEY (`rob_obj_xid` )
    REFERENCES `1gam201302`.`object` (`obj_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_room_fk`
    FOREIGN KEY (`rob_roo_xid` )
    REFERENCES `1gam201302`.`room` (`roo_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`update_file`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`update_file` (
  `upf_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `upf_path` VARCHAR(45) NOT NULL ,
  `upf_update_date` DATETIME NOT NULL ,
  PRIMARY KEY (`upf_id`) ,
  UNIQUE INDEX `upf_path_UNIQUE` (`upf_path` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 2
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- function get_dungeon
-- -----------------------------------------------------

DELIMITER $$
USE `1gam201302`$$
CREATE DEFINER=`thsempai`@`%` FUNCTION `get_dungeon`(nickname varchar(45)) RETURNS int(11)
begin

        declare dungeon_id int;
        declare user_id int;

        

        select 
            get_user(use_nickname)
        into
            user_id;

        return 1;

    end$$

DELIMITER ;

-- -----------------------------------------------------
-- function get_user
-- -----------------------------------------------------

DELIMITER $$
USE `1gam201302`$$
CREATE DEFINER=`thsempai`@`%` FUNCTION `get_user`(nickname varchar(45)) RETURNS int(11)
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
    end$$

DELIMITER ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
