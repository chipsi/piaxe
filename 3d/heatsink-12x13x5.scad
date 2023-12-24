color("#da8a67") difference() {
    cube([12, 13, 5], center=true);


    union() {
        for (i = [-2:2]) {
            translate([0, -2*i, 2]) cube([20, 1, 2.5], center=true);
            translate([-2*i, 0, 2]) cube([1, 20, 2.5], center=true);
        }
    }
}