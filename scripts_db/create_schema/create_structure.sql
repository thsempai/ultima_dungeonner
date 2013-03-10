SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `1gam201302` ;
CREATE SCHEMA IF NOT EXISTS `1gam201302` DEFAULT CHARACTER SET utf8 ;
USE `1gam201302` ;

-- -----------------------------------------------------
-- Table `1gam201302`.`dungeon`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`dungeon` (
  `dun_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `dun_date` DATE NULL DEFAULT NULL ,
  PRIMARY KEY (`dun_id`) )
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
  PRIMARY KEY (`til_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`object`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`object` (
  `obj_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `obj_name` VARCHAR(45) NOT NULL ,
  `obj_til_xid` INT(11) NOT NULL ,
  `obj_til_x` INT(11) NOT NULL ,
  `obj_til_y` INT(11) NOT NULL ,
  PRIMARY KEY (`obj_id`) ,
  INDEX `fk_tileset_fk` (`obj_til_xid` ASC) ,
  CONSTRAINT `fk_tileset_fk`
    FOREIGN KEY (`obj_til_xid` )
    REFERENCES `1gam201302`.`tileset` (`til_id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8;


-- -----------------------------------------------------
-- Table `1gam201302`.`user`
-- -----------------------------------------------------
CREATE  TABLE IF NOT EXISTS `1gam201302`.`user` (
  `use_id` INT(11) NOT NULL AUTO_INCREMENT ,
  `use_nickname` VARCHAR(45) NOT NULL ,
  `use_password` VARCHAR(45) NOT NULL ,
  PRIMARY KEY (`use_id`) ,
  UNIQUE INDEX `ndx_use_name` (`use_nickname` ASC) )
ENGINE = InnoDB
AUTO_INCREMENT = 5
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
  INDEX `fk_user_fk1` (`roo_use_xid` ASC) ,
  INDEX `fk_tileset_fk1` (`roo_til_xid` ASC) ,
  UNIQUE INDEX `ndx_roo_name` (`roo_name` ASC) ,
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
AUTO_INCREMENT = 2
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



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
