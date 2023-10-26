$fn=10;
a=8.1;
h=3.5;
color("#31aee1") difference() {
    union() {
        cube([40, 40, 1]);

        for (i=[0: 15]) {
            translate([0, 0.5+i*2.55, 0]) cube([40, 0.7, 25]);
        }
    }
    for (i=[0:3]) {
        tx = (i % 2) == 0 ? 0 : (40-a);
        ty = floor(i / 2) != 0 ? 0 : (40-a);
        translate([tx, ty, 1]) cube([a, a, 25]);
    }
    for (i=[0:3]) {
        tx = (i % 2) == 0 ? h : (40-h);
        ty = floor(i / 2) != 0 ? h : (40-h);
        translate([tx, ty, -1]) cylinder(d=3.2, h=10);
    }
    translate([20-1, 0, 1]) cube([1, 40, 25]);
    translate([20-1+12, 0, 1]) cube([1, 40, 25]);
    translate([20-1-12, 0, 1]) cube([1, 40, 25]);
}


