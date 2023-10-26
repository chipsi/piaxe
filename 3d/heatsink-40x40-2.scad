$fn=100;
a=8.1;
h=3.5;
color("#31aee1") difference() {
    union() {
        cube([40, 40, 2.2]);

        for (i=[0: 15]) {
            translate([0, 0.5+i*2.55, 0]) cube([40, 0.7, 25]);
        }
        translate([20, 20, 1.1]) rotate([0, 0, 45]) cube([71.6-8, 8, 2.2], center=true);
        translate([-2.5, -2.5, 1.1]) cylinder(d=8, h=2.2, center=true);
        translate([2.5+40, 2.5+40, 1.1]) cylinder(d=8, h=2.2, center=true);
    }
    translate([20-1, 0, 1]) cube([1, 40, 25]);
    translate([-2.5, -2.5, 1.0]) cylinder(d=3.5, h=2.5, center=true);
    translate([2.5+40, 2.5+40, 1.0]) cylinder(d=3.5, h=2.5, center=true);
}
