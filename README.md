# Text to unit generator

## About

This small script helps transforming unit abbreviatons mainly from [ToT Megasheet Of Solutions](https://docs.google.com/spreadsheets/d/1lp1PwicC9QwwQye32IwLriIV0H4OQcrcpWPYDbxeu30) to human viewable form

Can also be handy for generating images for guides

## Usage

You can currently use it online at [ef.apoapsis-web.tk](https://ef.apoapsis-web.tk/)

Unit string should be in the following format: `[T1-6]<Unit name or abbreviation>[(PI)/(MI)][*0-9223372036854775807]` (Although `*9223372036854775807` is totally not recommended for your pc)

Example string: `DK(PI) T3Gunner*3 T6DK(MI) Gunner`

Which will result in:

![Example image with units](public/example_image.png)

**NOTE: You can't use `T*` with `Sr` prefix**

## Table of contents

- [./public/units.json](public/units.json) : Unit data storage
- - `units`  : Array with all the units
- - - `name` : Unit name in english
- - - `star` : Defalut unit stars count
- - - `local` : Localized unit names, feel free to add new ones yourself
- [./public/normal/](public/normal) : Default unit skins
- [./public/senior/](public/senior) : Senior unit skin variants
- [./public/system/](public/system) : Sprites used by script to generate images
- - `*-star.png` : Unit backgrounds
- - [empty_unit.png](public/system/empty_unit.png) : Default unit background
- - [immune-m.png](public/system/immune-m.png) : Magic immunity sprite
- - [immune-p.png](public/system/immune-p.png) : Physical immunity sprite
- - [plus.png](public/system/plus.png) : Sprite for multiple units used in ToT, called by giving a unit T4-6
- - [tier.png](system/tier.png) : Unit transendance sprite
