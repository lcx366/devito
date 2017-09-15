from sympy import Eq, cos, sin

from devito import Operator, TimeData
from examples.seismic import PointSource, Receiver
from devito.finite_difference import centered, first_derivative, right, transpose
from devito.dimension import x, y, z, t, time


def Gxx_shifted(field, costheta, sintheta, cosphi, sinphi, space_order):
    Gx1 = (costheta * cosphi * field.dx + costheta * sinphi * field.dyr -
           sintheta * field.dzr)
    Gxx1 = (first_derivative(Gx1 * costheta * cosphi,
                             dim=x, side=centered, order=space_order,
                             matvec=transpose) +
            first_derivative(Gx1 * costheta * sinphi,
                             dim=y, side=right, order=space_order,
                             matvec=transpose) -
            first_derivative(Gx1 * sintheta,
                             dim=z, side=right, order=space_order,
                             matvec=transpose))
    Gx2 = (costheta * cosphi * field.dxr + costheta * sinphi * field.dy -
           sintheta * field.dz)
    Gxx2 = (first_derivative(Gx2 * costheta * cosphi,
                             dim=x, side=right, order=space_order,
                             matvec=transpose) +
            first_derivative(Gx2 * costheta * sinphi,
                             dim=y, side=centered, order=space_order,
                             matvec=transpose) -
            first_derivative(Gx2 * sintheta,
                             dim=z, side=centered, order=space_order,
                             matvec=transpose))
    return -.5 * (Gxx1 + Gxx2)


def Gxx_shifted_2d(field, costheta, sintheta, space_order):
    Gx1 = (costheta * field.dxr - sintheta * field.dy)
    Gxx1 = (first_derivative(Gx1 * costheta, dim=x,
                             side=right, order=space_order,
                             matvec=transpose) -
            first_derivative(Gx1 * sintheta, dim=y,
                             side=centered, order=space_order,
                             matvec=transpose))
    Gx2p = (costheta * field.dx - sintheta * field.dyr)
    Gxx2 = (first_derivative(Gx2p * costheta, dim=x,
                             side=centered, order=space_order,
                             matvec=transpose) -
            first_derivative(Gx2p * sintheta, dim=y,
                             side=right, order=space_order,
                             matvec=transpose))

    return -.5 * (Gxx1 + Gxx2)


def Gyy_shifted(field, cosphi, sinphi, space_order):
    Gyp = (sinphi * field.dx - cosphi * field.dyr)
    Gyy = (first_derivative(Gyp * sinphi,
                            dim=x, side=centered, order=space_order,
                            matvec=transpose) -
           first_derivative(Gyp * cosphi,
                            dim=y, side=right, order=space_order,
                            matvec=transpose))
    Gyp2 = (sinphi * field.dxr - cosphi * field.dy)
    Gyy2 = (first_derivative(Gyp2 * sinphi,
                             dim=x, side=right, order=space_order,
                             matvec=transpose) -
            first_derivative(Gyp2 * cosphi,
                             dim=y, side=centered, order=space_order,
                             matvec=transpose))
    return -.5 * (Gyy + Gyy2)


def Gzz_shited(field, costheta, sintheta, cosphi, sinphi, space_order):
    Gzr = (sintheta * cosphi * field.dx + sintheta * sinphi * field.dyr +
           costheta * field.dzr)
    Gzz = (first_derivative(Gzr * sintheta * cosphi,
                            dim=x, side=centered, order=space_order,
                            matvec=transpose) +
           first_derivative(Gzr * sintheta * sinphi,
                            dim=y, side=right, order=space_order,
                            matvec=transpose) +
           first_derivative(Gzr * costheta,
                            dim=z, side=right, order=space_order,
                            matvec=transpose))
    Gzr2 = (sintheta * cosphi * field.dxr + sintheta * sinphi * field.dy +
            costheta * field.dz)
    Gzz2 = (first_derivative(Gzr2 * sintheta * cosphi,
                             dim=x, side=right, order=space_order,
                             matvec=transpose) +
            first_derivative(Gzr2 * sintheta * sinphi,
                             dim=y, side=centered, order=space_order,
                             matvec=transpose) +
            first_derivative(Gzr2 * costheta,
                             dim=z, side=centered, order=space_order,
                             matvec=transpose))
    return -.5 * (Gzz + Gzz2)


def Gzz_shited_2d(field, costheta, sintheta, space_order):
    Gz1r = (sintheta * field.dxr + costheta * field.dy)
    Gzz1 = (first_derivative(Gz1r * sintheta, dim=x,
                             side=right, order=space_order,
                             matvec=transpose) +
            first_derivative(Gz1r * costheta, dim=y,
                             side=centered, order=space_order,
                             matvec=transpose))
    Gz2r = (sintheta * field.dx + costheta * field.dyr)
    Gzz2 = (first_derivative(Gz2r * sintheta, dim=x,
                             side=centered, order=space_order,
                             matvec=transpose) +
            first_derivative(Gz2r * costheta, dim=y,
                             side=right, order=space_order,
                             matvec=transpose))

    return -.5 * (Gzz1 + Gzz2)


def Gzz_centered(field, costheta, sintheta, cosphi, sinphi, space_order):
    order1 = space_order / 2
    Gz = -(sintheta * cosphi * first_derivative(field, dim=x,
                                                side=centered, order=order1) +
           sintheta * sinphi * first_derivative(field, dim=y,
                                                side=centered, order=order1) +
           costheta * first_derivative(field, dim=z,
                                       side=centered, order=order1))
    Gzz = (first_derivative(Gz * sintheta * cosphi,
                            dim=x, side=centered, order=order1,
                            matvec=transpose) +
           first_derivative(Gz * sintheta * sinphi,
                            dim=y, side=centered, order=order1,
                            matvec=transpose) +
           first_derivative(Gz * costheta,
                            dim=z, side=centered, order=order1,
                            matvec=transpose))
    return Gzz


def Gzz_centered_2d(field, costheta, sintheta, space_order):
    order1 = space_order / 2
    Gz = -(sintheta * first_derivative(field, dim=x, side=centered, order=order1) +
           costheta * first_derivative(field, dim=y, side=centered, order=order1))
    Gzz = (first_derivative(Gz * sintheta, dim=x,
                            side=centered, order=order1,
                            matvec=transpose) +
           first_derivative(Gz * costheta, dim=y,
                            side=centered, order=order1,
                            matvec=transpose))
    return Gzz


# Centered case produces directly Gxx + Gyy
def Gxxyy_centered(field, costheta, sintheta, cosphi, sinphi, space_order):
    Gzz = Gzz_centered(field, costheta, sintheta, cosphi, sinphi, space_order)
    return field.laplace - Gzz


def Gxx_centered_2d(field, costheta, sintheta, space_order):
    return field.laplace - Gzz_centered_2d(field, costheta, sintheta, space_order)


def kernel_shited_2d(u, v, costheta, sintheta, cosphi, sinphi, space_order):
    Gxx = Gxx_shifted_2d(u, costheta, sintheta, space_order)
    Gzz = Gzz_shited_2d(v, costheta, sintheta, space_order)
    return Gxx, Gzz


def kernel_shited_3d(u, v, costheta, sintheta, cosphi, sinphi, space_order):
    Gxx = Gxx_shifted(u, costheta, sintheta, cosphi, sinphi, space_order)
    Gyy = Gyy_shifted(u, cosphi, sinphi, space_order)
    Gzz = Gzz_shited(v, costheta, sintheta, cosphi, sinphi, space_order)
    return Gxx + Gyy, Gzz


def kernel_centered_2d(u, v, costheta, sintheta, cosphi, sinphi, space_order):
    Gxx = Gxx_centered_2d(u, costheta, sintheta, space_order)
    Gzz = Gzz_centered_2d(v, costheta, sintheta, space_order)
    return Gxx, Gzz


def kernel_centered_3d(u, v, costheta, sintheta, cosphi, sinphi, space_order):
    Gxx = Gxxyy_centered(u, costheta, sintheta, cosphi, sinphi, space_order)
    Gzz = Gzz_centered(v, costheta, sintheta, cosphi, sinphi, space_order)
    return Gxx, Gzz


def ForwardOperator(model, source, receiver, time_order=2, space_order=4,
                    save=False, kernel='centered', **kwargs):
    """
       Constructor method for the forward modelling operator in an acoustic media

       :param model: :class:`Model` object containing the physical parameters
       :param src: None ot IShot() (not currently supported properly)
       :param data: IShot() object containing the acquisition geometry and field data
       :param: time_order: Time discretization order
       :param: spc_order: Space discretization order

       Rotated centered laplacian based on the following assumptions:
       1 - Laplacian is rotation invariant.
       2 - We still need to implement the rotated version as
       the regular laplacian only look at the cartesian axxis
       3- We must have Hp + Hz = Laplacian

       Stencil goes as follow
       For Hp compute Hz and Hp = laplace - Hz
       For Hz compute directly Hz

       This guaranties that the diagonal of the operator will
       not be empty due to odd-even coupling. The FD operator
       is still self-adjoint for stability as both the laplacian and
       the implementation of Hp and Hz are self-adjoints

       The rotated dshifted laplacian is the average of two non-centered
       rotated laplacian. All rotated operators are implemented in that case
       """
    dt = model.critical_dt

    m, damp, epsilon, delta, theta, phi = (model.m, model.damp, model.epsilon,
                                           model.delta, model.theta, model.phi)

    # Create symbols for forward wavefield, source and receivers
    u = TimeData(name='u', shape=model.shape_domain, dtype=model.dtype,
                 save=save, time_dim=source.nt if save else None,
                 time_order=time_order, space_order=space_order)
    v = TimeData(name='v', shape=model.shape_domain, dtype=model.dtype,
                 save=save, time_dim=source.nt if save else None,
                 time_order=time_order, space_order=space_order)
    src = PointSource(name='src', ntime=source.nt, ndim=source.ndim,
                      npoint=source.npoint)
    rec = Receiver(name='rec', ntime=receiver.nt, ndim=receiver.ndim,
                   npoint=receiver.npoint)

    # Tilt and azymuth setup
    ang0 = cos(theta)
    ang1 = sin(theta)
    ang2 = 0
    ang3 = 0
    if len(model.shape) == 3:
        ang2 = cos(phi)
        ang3 = sin(phi)

    FD_kernel = kernels[(kernel, len(model.shape))]
    H0, Hz = FD_kernel(u, v, ang0, ang1, ang2, ang3, space_order)
    s = t.spacing
    # Stencils
    stencilp = 1.0 / (2.0 * m + s * damp) * \
        (4.0 * m * u + (s * damp - 2.0 * m) *
         u.backward + 2.0 * s ** 2 * (epsilon * H0 + delta * Hz))
    stencilr = 1.0 / (2.0 * m + s * damp) * \
        (4.0 * m * v + (s * damp - 2.0 * m) *
         v.backward + 2.0 * s ** 2 * (delta * H0 + Hz))
    first_stencil = Eq(u.forward, stencilp)
    second_stencil = Eq(v.forward, stencilr)
    stencils = [first_stencil, second_stencil]

    # SOurce and receivers
    stencils += src.inject(field=u.forward, expr=src * dt * dt / m,
                           offset=model.nbpml)
    stencils += src.inject(field=v.forward, expr=src * dt * dt / m,
                           offset=model.nbpml)
    stencils += rec.interpolate(expr=u + v, offset=model.nbpml)
    # Add substitutions for spacing (temporal and spatial)
    subs = dict([(t.spacing, dt)] + [(time.spacing, dt)] +
                [(i.spacing, model.get_spacing()[j]) for i, j
                 in zip(u.indices[1:], range(len(model.shape)))])
    # Operator
    return Operator(stencils, subs=subs, name='ForwardTTI', **kwargs)


kernels = {('shifted', 3): kernel_shited_3d, ('shifted', 2): kernel_shited_2d,
           ('centered', 3): kernel_centered_3d, ('centered', 2): kernel_centered_2d}
