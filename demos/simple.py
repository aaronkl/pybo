import numpy as np
import matplotlib.pyplot as pl

import pygp as pg
import pybo.models as pbm
import pybo.policies as pbp


def run_model(Policy, Model, sn, ell, sf, T):
    model = Model(sn)
    gp = pg.BasicGP(sn, ell, sf)
    policy = Policy(gp, model.bounds)

    xmin = model.bounds[0,0]
    xmax = model.bounds[0,1]
    X = np.linspace(xmin, xmax, 200)[:, None]
    x = (xmax-xmin) / 2 + xmin

    for i in xrange(T):
        pg.gpplot(policy.gp, xmin=xmin, xmax=xmax, draw=False)

        pl.plot(X, policy.get_index(X), lw=2)
        pl.axvline(x, color='r')
        pl.axis('tight')
        pl.axis(xmin=xmin, xmax=xmax)
        pl.draw()

        y = model.get_data(x)
        policy.add_data(x, y)
        x = policy.get_next()


if __name__ == '__main__':
    run_model(pbp.Thompson, pbm.Gramacy, 0.2, 0.05, 1.25, 100)
