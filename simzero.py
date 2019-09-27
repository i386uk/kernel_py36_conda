# simple animation helper

d_n = 0


def init(dim, n_part):
    global d_n
    if dim not in [1, 2, 3]:
        raise Exception('We only support simulations in dimension 1,2, or 3')
    d_n = dim*n_part
    print(dim, n_part)


def add(coords):
    # process positions at a single timestep
    # reformat all coordinates as
    # . rx1,ry1,rz1,rx2,ry2,rz2,..
    # . single precision
    # and print to stdout
    if len(coords) != d_n:
        raise Exception('Mismatch in the number of coords')
    print(','.join('{:8.3f}'.format(r) for r in coords))


if __name__ == "__main__":
    init(3, 2)
    add([2/3, 3/4])
