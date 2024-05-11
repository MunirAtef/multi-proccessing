import numpy as np
import matplotlib.pyplot as plt
import math


class PolyFun:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def __call__(self, x):
        # (self, x):
        value = 0
        for i in range(len(self.coefficients)):
            value += self.coefficients[i] * x ** i
        return value

    def mul(self, n):
        return PolyFun([i * n for i in self.coefficients])

    def __add__(self, other):
        self_len = len(self.coefficients)
        other_len = len(other.coefficients)

        res_coe = []

        # [5, 4, 2, 3]
        # [9, 2]
        for i in range(min(self_len, other_len)):
            res_coe.append(self.coefficients[i] + other.coefficients[i])

        if self_len > other_len:
            res_coe += self.coefficients[other_len:]
        else:
            res_coe += other.coefficients[self_len:]

        return PolyFun(res_coe)

    def __str__(self):
        return str(self.coefficients)

    def avg(self, other):
        return (self + other).mul(0.5)

    def plot(self, interval):
        y = [self(i) for i in interval]
        plt.plot(interval, y)


class PopObject:
    def __init__(self, test_poly: PolyFun, target_poly: PolyFun, interval):
        pos = 0
        neg = 0
        for i in interval:
            error = test_poly(test_poly(i)) - target_poly(i)
            if error > 0:
                pos += error
            else:
                neg += error

        self.pf = test_poly
        self.unsigned_fit = (pos - neg) / len(interval)
        self.signed_fit = (pos + neg) / len(interval)

        # print(self.unsigned_fit)

    def __str__(self):
        return f"fitness: {self.unsigned_fit}, \tpoly: {self.pf}"


class GA:
    def __init__(self, squared_func: PolyFun, interval):
        self.squared_func = squared_func
        self.interval = interval
        self.pop_size = 50
        self.population = []
        self.best_ever = PolyFun([])

    def init_population(self):
        for i in np.linspace(0, 1, self.pop_size):
            pop = self.squared_func.mul(i) + PolyFun([0, 1 - i])
            self.population.append(PopObject(pop, self.squared_func, self.interval))
            print(pop)

        self.population.sort(key=lambda p: p.unsigned_fit)
        for i in self.population:
            print(i)
        # print(self.population)

    def fitness(self, pf: PolyFun):
        pos = 0
        neg = 0

        for i in self.interval:
            error = pf(pf(i)) - self.squared_func(i)
            if error > 0:
                pos += error
            else:
                neg += error

        return pos, neg


class PointCurve:
    # if    (a, b)       belongs   g(x)
    # then  (b, f(a))    belongs   g(x)
    def __init__(self, x, y):
        pass


def next_point(a, b, squared_func: PolyFun):
    return b, squared_func(a)


def point_line(a, b, squared_func: PolyFun):
    h = 0.001
    return a + h, (squared_func(a) - b) / (b - a) * h + b


def archive():
    squared_func = PolyFun([0, 0, 1])  # x^2

    interval = np.linspace(2, 4, 50)
    plt.plot(interval, [i ** (2 ** 0.5) for i in interval])

    # for i in np.linspace(0, 4, 10):
    #     for j in np.linspace(0, 4, 10):
    #         nxp = next_point(i, j, squared_func)
    #         plt.scatter((i + nxp[0])/2, (j + nxp[1])/2, linewidth=1)
    #         plt.plot([i, nxp[0]], [j, nxp[1]], linewidth=0.5)

    # plt.show()
    # return

    pox = []
    poy = []
    cp = (2, 2 ** (2 ** 0.5) - 0.1)
    end = next_point(cp[0], cp[1], squared_func)

    for i in np.linspace(0, 1, 20):
        cp0 = cp[0] * i + end[0] * (1 - i)
        cp1 = cp[1] * i + end[1] * (1 - i)

        nx = next_point(cp0, cp1, squared_func)

        plt.plot([cp0, nx[0]], [cp1, nx[1]], color="red", linewidth=0.5)

    end_nx = next_point(*end, squared_func)
    plt.plot([cp[0], end_nx[0]], [cp[1], end_nx[1]], color="purple", linewidth=1)
    plt.show()
    return

    for i in range(1000):
        pox.append(cp[0])
        poy.append(cp[1])
        cp = point_line(cp[0], cp[1], squared_func)

    plt.plot(pox, poy)
    plt.show()
    return
    rp = (1, 2)
    nxt = next_point(rp[0], rp[1], squared_func)

    for i in range(10):
        nxt = next_point(rp[0], rp[1], squared_func)
        rp = ((rp[0] + nxt[0]) / 2, (rp[1] + nxt[1]) / 2)
        print(rp, "\t\t", rp[0] ** (2 ** 0.5))


class FunDNA:
    def __init__(self, dna: list[float]):
        self.dna = dna
        self.h = 1 / (len(dna) - 1)

    def __call__(self, *args, **kwargs):
        v = args[0]
        lower = math.floor(v / self.h)
        upper = math.ceil(v / self.h)

        if lower == upper:
            return self.dna[lower]

        m1 = v - lower * self.h
        m2 = upper * self.h - v

        return (self.dna[lower] * m2 + self.dna[upper] * m1) / (m1 + m2)

    def __len__(self):
        return len(self.dna)


def zig():
    interval = np.linspace(0, 1, 10)

    fd = FunDNA([i for i in interval])
    sd = FunDNA([i + 1 for i in interval])

    sf_list = []
    length = len(fd)
    for i in range(length):
        sf_list.append(f(fd(i / length)))

    print(sf_list)


def f(x):
    return x ** 2


def fd(x):
    return 2 * x


def inv(x):
    return x ** 0.5


def next_ys(xs: list, ys: list):
    # n = 0.5
    deg = len(xs) - 1
    coe_fun = list(np.polyfit(xs, ys, deg))
    coe_inv = list(np.polyfit(ys, xs, deg))

    new_ys = []
    for i in xs:
        t1 = np.polyval(coe_fun, i)
        t2 = f(np.polyval(coe_inv, i))

        # new_ys.append((1 - n) * t1 + n * t2)
        new_ys.append((t1 + t2) / 2)

    return new_ys


def bsm_allah():
    xs = list(np.linspace(0, 1, 10))
    ys = xs.copy()

    plt.plot(xs, [i ** (2 ** 0.5) for i in xs], color="purple")

    for i in range(50):
        ys = next_ys(xs, ys)

    coe = np.polyfit(xs, ys, len(xs) - 1)

    val = np.polyval(coe, 0.3)
    print(val)
    print(0.3 ** (2 ** 0.5))
    plt.plot(xs, ys)

    plt.show()


def ya_allah():
    x = 3
    p = 7
    m = 2

    print(p)
    for i in range(50):
        v = x + (x - p) / m
        p = (p + f(v)) / 2
        m = m / 2 + fd(v) / (2 * m)

        print(p)


# loop from starting point to end point and draw the opposite point for each one
def curve_from_line(a, b, pf: PolyFun):
    na, nb = b, pf(a)

    xs = []
    ys = []
    for i in np.linspace(0, 1, 100):
        ca, cb = (1 - i) * a + i * na, (1 - i) * b + i * nb
        xs.append(cb)
        ys.append(pf(ca))

    plt.plot(xs, ys)


def integral_curve(a, b, pf: PolyFun):
    na, nb = b, pf(a)
    i = 0.01
    return (1 - i) * a + i * na, (1 - i) * b + i * nb

def loop_to_integral(a, b, pf, color):
    xs = []
    ys = []

    for i in range(100):
        xs.append(a)
        ys.append(b)
        a, b = integral_curve(a, b, pf)

    plt.plot(xs, ys, color=color)
    # return xs, ys


def main():
    squared_func = PolyFun([0, 0, 1])  # 1 + x^2
    # squared_func.plot(np.linspace(0, 5, 100))
    interval = np.linspace(0, 5, 100)
    plt.plot(interval, [i ** (2 ** 0.5) for i in interval])

    a, b = 2, 2**(2**0.5)
    # curve_from_line(a, b, squared_func)
    # loop_to_integral(a, b + 0.1, squared_func, "red")
    loop_to_integral(a, b, squared_func, "green")
    # loop_to_integral(a, b - 0.1, squared_func, "blue")

    # plt.scatter(a, b, color="red")
    # plt.scatter(b, squared_func(a), color="green")
    plt.show()
    return

    best_ever = PolyFun([])
    interval = list(np.linspace(0, 100, 100))
    # ga = GA(squared_func, interval)
    # ga.init_population()
    # print(g)

    px, py = generate_fun(1, 1, squared_func)

    coeffs = np.polyfit(px, py, len(px) - 1)
    PolyFun(coeffs).plot(interval)
    plt.plot(px, py)

    plt.show()


if __name__ == '__main__':
    main()
