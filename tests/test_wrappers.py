from __future__ import absolute_import
import autograd.numpy as np
import autograd.numpy.random as npr
from autograd.util import *
from autograd import (grad, elementwise_grad, jacobian, value_and_grad,
                      grad_and_aux, hessian_vector_product, hessian, multigrad)
npr.seed(1)

def test_hessian():
    # Check Hessian of a quadratic function.
    D = 5
    H = npr.randn(D, D)
    def fun(x):
        return np.dot(np.dot(x, H),x)
    hess = hessian(fun)
    x = npr.randn(D)
    check_equivalent(hess(x), H + H.T)

def test_multigrad():
    def complicated_fun(a,b,c,d,e,f=1.1, g=9.0):
        return a + np.sin(b) + np.cosh(c) + np.cos(d) + np.tan(e) + f + g

    def complicated_fun_3_1(d, b):
        return complicated_fun(A, b, C, d, E, f=F, g=G)

    A = 0.5
    B = -0.3
    C = 0.2
    D = -1.1
    E = 0.7
    F = 0.6
    G = -0.1

    exact = multigrad(complicated_fun, argnums=[3, 1])(A, B, C, D, E, f=F, g=G)
    numeric = nd(complicated_fun_3_1, D, B)
    check_equivalent(exact, numeric)


def test_elementwise_grad():
    def simple_fun(a):
        return a + np.sin(a) + np.cosh(a)

    A = npr.randn(10)

    exact = elementwise_grad(simple_fun)(A)
    numeric = np.squeeze(np.array([nd(simple_fun, A[i]) for i in xrange(len(A))]))
    check_equivalent(exact, numeric)


def test_elementwise_grad_multiple_args():
    def simple_fun(a, b):
        return a + np.sin(a) + np.cosh(b)

    A = 0.9
    B = npr.randn(10)
    argnum = 1

    exact = elementwise_grad(simple_fun, argnum=argnum)(A, B)
    numeric = np.squeeze(np.array([nd(simple_fun, A, B[i])[argnum] for i in xrange(len(B))]))
    check_equivalent(exact, numeric)
