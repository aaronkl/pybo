import numpy as np
import matplotlib.pyplot as pl

import pygp
import pybo.solvers.policies.entropy as entropy
import pybo.solvers.policies.entropy2 as entropy2


if __name__ == '__main__':
    gp = pygp.BasicGP(sn=0.1, ell=0.05, sf=1, kernel='matern3')

    rng = pygp.utils.random.rstate(0)
    X = rng.rand(20, 1)
    y = gp.sample(X, latent=False, rng=rng)
    z = np.array([0.8])

    gp = pygp.BasicGP(sn=0.1, ell=0.25, sf=1)
    gp.add_data(X, y)
    pygp.optimize(gp)

    # get the test locations.
    xx = np.linspace(X.min(), X.max(), 200)
    Xtest = xx[:, None]

    # get the "prior" predictions.
    mu_, s2_ = gp.posterior(xx[:, None])
    er_ = 2*np.sqrt(s2_)

    # get the "posterior" predictions.
    mu, s2 = entropy.predict(gp, z, Xtest)
    er = 2*np.sqrt(s2)

    muo, s2o = entropy2.predict_ep(Xtest, gp._X, gp._y, z,
                                   np.exp(gp._kernel._logell),
                                   np.exp(gp._kernel._logsf*2),
                                   gp._likelihood.s2)
    ero = 2*np.sqrt(s2o)

    pl.figure(1)
    pl.clf()

    color = next(pl.gca()._get_lines.color_cycle)
    pl.plot(xx, mu_, color=color, lw=2, label='prior')
    pl.fill_between(xx, mu_+er_, mu_-er_, color=color, alpha=0.15)

    color = next(pl.gca()._get_lines.color_cycle)
    pl.plot(xx, mu, color=color, lw=2, label='posterior')
    pl.fill_between(xx, mu+er, mu-er, color=color, alpha=0.15)

    color = next(pl.gca()._get_lines.color_cycle)
    pl.plot(xx, muo, color=color, lw=2, label='posterior old')
    pl.fill_between(xx, muo+ero, muo-ero, color=color, alpha=0.15)

    pl.scatter(X, y, label='data', marker='o', facecolors='none', s=30, lw=1,
               color='k', zorder=3)

    pl.legend(loc='best')
    pl.axis('tight')
    pl.draw()
    pl.show()
