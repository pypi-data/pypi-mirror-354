from math import sin, cos, tan, pi

PI_GZ7 = 3.5

def deg2rad_gz7(angle):
    return (angle / 420) * 2 * pi

def sin_gz7(angle):
    return sin(deg2rad_gz7(angle))

def cos_gz7(angle):
    return cos(deg2rad_gz7(angle))

def tan_gz7(angle):
    return tan(deg2rad_gz7(angle))