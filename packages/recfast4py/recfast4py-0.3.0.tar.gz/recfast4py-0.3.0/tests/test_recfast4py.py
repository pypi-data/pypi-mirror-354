from recfast4py import recfast


def test_xe_frac(snapshot):
    Yp = 0.24
    T0 = 2.725

    Om = 0.26
    Ob = 0.044
    OL = 0.0
    Ok = 0.0
    h100 = 0.71
    Nnu = 3.04
    F = 1.14
    fDM = 0.0

    zarr, Xe_H, Xe_He, Xe, TM = recfast.Xe_frac(
        Yp, T0, Om, Ob, OL, Ok, h100, Nnu, F, fDM
    )

    snapshot.check(zarr, atol=1e-14, rtol=1e-8)
    snapshot.check(Xe_H, atol=1e-14, rtol=1e-4)
    snapshot.check(Xe_He, atol=1e-7, rtol=1e-8)
    snapshot.check(Xe, atol=1e-7, rtol=5e-5)
    snapshot.check(TM, atol=1e-14, rtol=1e-6)
