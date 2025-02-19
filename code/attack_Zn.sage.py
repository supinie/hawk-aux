

# This file was *autogenerated* from the file attack_Zn.sage
from sage.all_cmdline import *   # import sage library

_sage_const_20 = Integer(20); _sage_const_1 = Integer(1); _sage_const_0 = Integer(0); _sage_const_1p = RealNumber('1.'); _sage_const_2 = Integer(2); _sage_const_300 = Integer(300); _sage_const_0p000001 = RealNumber('0.000001'); _sage_const_p5 = RealNumber('.5'); _sage_const_40 = Integer(40)# within my sage environment multiprocessing had a bug so I had to separate
# the functions into a separate file, _attack_Zn.sage
# NOTE: if you make changes you must
# $ sage --preparse _attack_Zn.sage
# $ mv _attack_Zn.sage.py _attack_Zn.py

# for g6k=True to work you must be able to e.g.
# $ sage
# $ import g6k
# without errors

from sage.all import log, prod

from multiprocessing import Pool

from _attack_Zn import one_experiment, one_experiment_structured

import os


def many_experiment(experiments, processes, n, sigma=_sage_const_20 , tours=_sage_const_1 , dual=False,
                    randomise=False, float_type="double", g6k=False):
    jobs = [(n, seed, sigma, tours, dual, randomise, float_type, g6k) for seed in range(experiments)] # noqa
    with Pool(processes) as p:
        res = p.map(one_experiment, jobs)
    res = [x for x in res if x is not None]
    if not len(res):
        return _sage_const_0 , _sage_const_0 
    return [x[_sage_const_0 ] for x in res]
    # avg_b = float(sum([x[0] for x in res])/len(res))
    # avg_normalised_prevnorm = float(sum([x[1] for x in res])/len(res))
    # geo_normalised_prevnorm = float(prod([x[1] for x in res]))**(1./len(res))
    # profiles = [x[2] for x in res]
    # return avg_b, avg_normalised_prevnorm, geo_normalised_prevnorm, profiles


def many_experiment_structured(experiments, processes, n, sigma=_sage_const_20 , tours=_sage_const_1 ,
                               dual=False, randomise=False,
                               float_type="double", g6k=False, hawk=True):
    jobs = [(n, seed, sigma, tours, dual, randomise, float_type, g6k, hawk) for seed in range(experiments)] # noqa
    with Pool(processes) as p:
        res = p.map(one_experiment_structured, jobs)
    res = [x for x in res if x is not None]
    if not len(res):
        return _sage_const_0 , _sage_const_0 
    avg_b = float(sum([x[_sage_const_0 ] for x in res])/len(res))
    avg_normalised_prevnorm = float(sum([x[_sage_const_1 ] for x in res])/len(res))
    geo_normalised_prevnorm = float(prod([x[_sage_const_1 ] for x in res]))**(_sage_const_1p /len(res))
    profiles = [x[_sage_const_2 ] for x in res]
    return avg_b, avg_normalised_prevnorm, geo_normalised_prevnorm, profiles


def make_plots(profiles, basename="bkz-gso-norms", extension="png", dpi=_sage_const_300 ,
               extra=None):
    # with compliments to martin
    import matplotlib.pyplot as plt

    if extra is None:
        extra = ""
    else:
        os.chdir(extra)

    def profiles_sanity(profiles):
        for (key, gso_norms) in profiles.items():
            for i in range(len(gso_norms)):
                if gso_norms[i] < _sage_const_0 :
                    gso_norms[i] = _sage_const_0p000001 
            profiles[key] = gso_norms

    def maplog2(sqr_gso_norms):
        return [log(x, _sage_const_2 ) for x in sqr_gso_norms]

    profiles_sanity(profiles)

    def plot_finalise(ax, name):
        ax.set_ylabel("$2\\,\\log_2(\\cdot)$")
        ax.set_xlabel("$i$")
        ax.legend(loc="upper right")
        ax.set_ylim(*ylim)

        fullname = "%s.%s" % (name, extension)
        fig.savefig(fullname, dpi=dpi)
        plt.close()

    d = len(profiles[_sage_const_0 ])
    x = range(d)

    simple_projections = [((d - i) / d)**_sage_const_p5  for i in range(d)]

    for b in profiles.keys():
        fig, ax = plt.subplots()
        ax.plot(x, maplog2(profiles[b]), label="$\\|\\mathbf{b}_i^*\\|$")
        ax.plot(x, maplog2(simple_projections), label="projection canonical")
        ylim = ax.get_ylim()
        ax.set_title("beta = {beta} {extra}".format(beta=str(b),
                                                    extra=extra))
        name = "{beta}-{basename}-{extra}".format(beta=str(b),
                                                  basename=basename,
                                                  extra=extra)
        plot_finalise(ax, name)


def average_profiles(many_profiles, until_block=_sage_const_40 , basename="avg_gso_norms",
                     extra=None):
    avg_profile = {}
    dimension = len(many_profiles[_sage_const_0 ][_sage_const_0 ])

    for b in range(until_block + _sage_const_1 ):
        if b == _sage_const_1 :
            continue
        num_profiles = sum([b in profile.keys() for profile in many_profiles])
        avg_profile_b = [_sage_const_1 ] * dimension
        for profile in many_profiles:
            try:
                for i in range(len(profile[b])):
                    gs_length_i = profile[b][i]
                    avg_profile_b[i] *= (gs_length_i**(_sage_const_1p /num_profiles))
            except KeyError:
                pass
        avg_profile[b] = avg_profile_b

    if extra is not None:
        extra_exists = os.path.isdir(extra)
        if not extra_exists:
            os.mkdir(extra)

    make_plots(avg_profile, basename=basename, extra=extra)

