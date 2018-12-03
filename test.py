# sp.init_printing()
l_x, l_y, a, a_i, θ_O, θ_Oi, θ_Of, t, t_i, t_f = sp.symbols('l_x, l_y, a, a_i, θ_O, θ_Oi, θ_Of, t, t_i, t_f')

"""Constraint Equation of Circle offset to Pt_0 AKA t_i """
CIRC = sp.Matrix([a*(sp.cos(t) - sp.cos(t_i)), 
                  a*(sp.sin(t) - sp.sin(t_i)),
                 1])
CIRC


"""Rotation around P_0 AKA t_i"""
# Convention is for z-, not z+ for CCW--> so '-θ_O'

CIRC_ROT1 = sp.rot_axis3(-θ_O)*(CIRC); CIRC_ROT1

""" 
Translate back to circle origin 
based off original circle radius 
"""
CIRC_ROT1_TRAN1 = sp.Matrix(
    [[1, 0, a_i*sp.cos(t_i)],
    [0, 1, a_i*sp.sin(t_i)],
    [0, 0, 1]]) * CIRC_ROT1
CIRC_ROT1_TRAN1


""" "a" as a function of θ_O """ 
# ri = idler radius
# a = radius of circle
# n = number of idlers
# θi = angle between idlers
a_f, ri, θi, n = sp.symbols('a_f, ri, θi, n')

θi = (t_f - t_i) / n

a_f = ri * sp.sin(θi/2)
t_fFt_i = 3*sp.pi - t_i #symmetric across y-axis
#aFθ_O = -20*sp.Abs(a_f-a_i)/(θ_Of) * θ_O + a_i; aFθ_O # linear relationship
#aFθ_O = sp.Abs(a_i-a_f)/(θ_Of-θ_O) + a_f; aFθ_O
aFθ_O = θ_O+a_i; aFθ_O


""" Final Curve """
CIRC_ROT1_TRAN2 = CIRC_ROT1_TRAN1.subs([(a, aFθ_O), (t_f, t_fFt_i)]); CIRC_ROT1_TRAN2

# Constants
t_iS = sp.pi * 7/6
t_fFt_iS = t_fFt_i.subs([(t_i, t_iS)])
a_iS = 12
riS = 0.5
θ_OfS = 90*sp.pi/180
θ_OS = sp.pi/4
nS = 4
sp.lambdify(t,t_iS)(1)
θiS = θi.subs([
    (t_i, t_iS),
    (t_f, t_fFt_iS),
    (n, nS)
]); θiS
a_fS = a_f.subs([
    (ri, riS),
    (θi,θiS)
])
aFθ_OS = aFθ_O.subs([
    (a_i, a_iS),
    (a_f, a_fS),
    (θ_Of, θ_OfS),
])

tArrPts = [t_iS, 
                    t_iS + θiS, 
                    t_iS + 2*θiS, 
                    t_iS + 3*θiS,
                    t_iS + 4*θiS
                    ]; tArrPts


""" Substitute all Constants """
CIRC_ROT1_TRAN2_S = CIRC_ROT1_TRAN2.subs([
    (t_i, t_iS),
    (a_i, a_iS),
    (ri, riS),
    (θ_Of, θ_OfS), 
    #(θ_O, θ_OS),
    #(t, tArrPts[3]),
    (n, nS)
])
CIRC_ROT1_TRAN2_S


x, y = sp.symbols('x, y')
CO = sp.collect(sp.expand(CIRC_ROT1_TRAN2_S[0] - x),(sp.cos(θ_O), sp.sin(θ_O)),evaluate=False)
A = CO[sp.cos(θ_O)]
B = CO[sp.sin(θ_O)]
C = CO[1]
sp.expand(CIRC_ROT1_TRAN2_S[0] - x)
#t_solv = sp.trigsimp(sp.simplify(sp.atan(B/A) + sp.acos(C/sp.sqrt(A**2 + B**2))))
#t_solv
#CIRC_F_X = CIRC_ROT1_TRAN2_S[1].subs([
#    (t, t_solv)])
#CIRC_F_X


""" Lamdify """
from sympy.utilities.lambdify import implemented_function, lambdify

f = lambdify((t, θ_O), CIRC_ROT1_TRAN2_S, modules=["numpy"])
#dir(f)
dir(CIRC_ROT1_TRAN2_S)
CIRC_ROT1_TRAN2_S.free_symbols
