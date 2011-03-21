#! /usr/bin/python
import Image;
import sys;
import math;

def mag(p):
    """Computes the magnitude of the given vector."""
    sum = 0;
    for x in p:
        sum += x*x;
    return math.sqrt(sum);

def diff(p1,p2):
    """Computes the difference between the two points. Assumes len(p1)==len(p2)."""
    return [ p1[i]-p2[i] for i in range(len(p1)) ];

def dist(p1,p2):
    """Computes the euclidean distance between the two points. Assumes len(p1)==len(p2)."""
    return mag(diff(p1,p2));

def main(argv=None):
    """Detects eyes in the input image and colors them in the output image."""
    # Acquire commandline
    if argv == None:
        argv = sys.argv;

    # Choose input file and output file
    input = None;
    output = None;

    if len(argv) > 1:
        input = argv[1];
        if len(argv) > 2:
            output = argv[2];

    if input == None:
        input = raw_input('Input File: ');

    if output == None:
        output = raw_input('Output File: ');

    # Load and display input image
    image = Image.open(input).convert('RGB');
    image.show();

    # Convert image to grayscale
    grayscale = image.convert('L');
    grayscale.show();

    # Save image dimensions
    width = image.size[0];
    height = image.size[1];

    # Construct hough dictionary
    populardarkareas = {};

    # Use some arbitrary intensity threshold (tunable parameter)
    intensity_threshold = 75;

    # Use some arbitrary radius (tunable parameter)
    radius = 20;

    # Contribute votes based on dark areas (we are looking for the pupil)
    for x in range(width):
        for y in range(height):
            if grayscale.getpixel((x, y)) < intensity_threshold:
                for xvote in range(max(0, x-radius), min(width, x+radius)):
                    miny=max(0, y-radius);
                    maxy=min(height, y+radius);
                    for yvote in range(miny, maxy):
                        xdiff=float(abs(xvote-x));
                        ydiff=float(abs(yvote-y));
                        rsq=xdiff*xdiff+ydiff*ydiff;
                        if (xvote, yvote) in populardarkareas:
                            if rsq == 0.0:
                                populardarkareas[(xvote, yvote)]+=1.0;
                            else:
                                delta = 1.0/rsq;
                                populardarkareas[(xvote, yvote)]+=delta;
                        else:
                            populardarkareas[(xvote, yvote)]=1.0;

    # Use some arbitrary vote threshold (tunable parameter)
    hough_threshold = 18.0;

    # Extract points with weights above the given threshold
    hough_points = set([]);
    for pair in populardarkareas:
        weight = populardarkareas[pair];
        if weight > hough_threshold:
            hough_points.add(pair);

    # Use some arbitrary highlight color (user preference)
    highlight_color = (125, 255, 125);

    # Construct a copy of the image and highlight areas believed to be a pupil
    highlighted_image = image.copy();
    for point in hough_points:
        highlighted_image.putpixel(point, highlight_color);
    highlighted_image.show();
    
    # Group the hough points together to find the eye center points
    eye_center_points = set([]);
    oldlen=len(hough_points);
    newlen=0;
    while oldlen!=newlen:
        oldlen = len(hough_points);
        eye_center_points = set([]);
        totals = {};
        mean = 0;
        # Points that are close together are probably a part of the same
        # group. Find their center via a weighted mean
        while len(hough_points) > 0:
            total = 1;
            current = hough_points.pop();
            wt = populardarkareas[current];
            xsum = wt*current[0];
            ysum = wt*current[1];
            wtsum = wt;
            for pt in hough_points.copy():
                if dist(current,pt) <= 3*radius:
                    total += 1;
                    wt = populardarkareas[pt];
                    xsum += wt*pt[0];
                    ysum += wt*pt[1];
                    wtsum += wt;
                    hough_points.remove(pt);
            x = int(float(xsum) / float(wtsum));
            y = int(float(ysum) / float(wtsum));
            wt = float(wtsum) / float(total);
            populardarkareas[(x, y)] = wt;
            eye_center_points.add((x, y));
            mean += total;
            totals[(x, y)] = total;
        # Groups that have very few elements contributing
        # to them are most likely outliers and should be removed
        mean = float(mean)/float(len(eye_center_points));
        for pt in eye_center_points.copy():
            if totals[pt] < (0.4*mean):
                eye_center_points.remove(pt);
        # Update values for next iteration
        hough_points = eye_center_points;
        newlen = len(hough_points);
    
    # Construct a copy of the image so that we can show where the eyes are:
    result = image.copy();
    
    # Draw squares around each of the eye center points in the result
    for eyecenter in eye_center_points:
        print eyecenter;
        minx=min(max(0,eyecenter[0]-3*radius),width);
        miny=min(max(0,eyecenter[1]-3*radius),height);
        maxx=max(min(eyecenter[0]+3*radius,width-1),0);
        maxy=max(min(eyecenter[1]+3*radius,height-1),0);
        for x in range(minx,maxx):
            result.putpixel((x, miny),highlight_color);
            result.putpixel((x, maxy),highlight_color);
        for y in range(miny,maxy):
            result.putpixel((minx, y),highlight_color);
            result.putpixel((maxx, y),highlight_color);
    
    # Show the result before we save it
    result.show();
    
    # Save the result
    result.save(output);

    # Return status code
    return 0;


if __name__ == "__main__":
    exit(main(sys.argv));
