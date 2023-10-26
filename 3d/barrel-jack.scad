$fn=50;

color("#404040") difference() {
    union() {
        translate([0, 0, 6]) rotate([0,90,0]) cylinder(d=8, h=13.5);
        translate([0, -4.5, 0]) cube([3.5, 9, 11]);
        translate([0, -4.5, 0]) cube([14.5, 9, 3.5]);
    }
    translate([-1, 0, 6]) rotate([0,90,0]) cylinder(d=6.4, h=14);
}

color("gray") translate([1, 0, 6]) rotate([0,90,0]) cylinder(d=2.5, h=12);

color("gray") {
//    translate([7.7, 0, -3.5]) cylinder(d=1, h=3.5);
//    translate([7.7 + 6, 0, -3.5]) cylinder(d=1, h=3.5);
//    translate([7.7 + 3, -4.7, -3.5]) cylinder(d=1, h=6.5);

    translate([7.7, 0, -3.5/2]) cube([0.5, 1, 3.5], center=true);
    translate([7.7 + 6, 0, -3.5/2]) cube([0.5, 1, 3.5], center=true);
    translate([7.7 + 3, -4.7, -6.5/2]) cube([1, 0.5, 6.5]);
    
    
    
}