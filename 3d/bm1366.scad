union() {
    color("#505050") cube([7, 6, 0.6], center=true);
    color("#a0a0a0") translate([0,0,0.3]) cube([3.5, 5.5, 0.01], center=true);
    color("#a0a0a0") translate([3,2.5,0.3]) cylinder(d=0.5, h=0.01);
}
    